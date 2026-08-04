"""Detector (1): Photo forensics - the highest value-per-line item in SAAKSHI.

CAG (Karnataka MGNREGA, 2026) found that identical photographs were uploaded
across different construction stages to fake progress. They found it by LOOKING,
in a 39-panchayat sample. We find it with a perceptual hash, across the whole
corpus, deterministically.

Four checks:
  (a) near-duplicate detection via a difference-hash (dHash) over the corpus
  (b) EXIF GPS vs the work's declared location  (a completion photo 60 km away)
  (c) EXIF timestamp outside the work's sanction..completion window
  (d) device clustering - one phone geo-tagging N sites inside one hour

Production (PLAN.md) uses `imagehash` pHash on real JPEGs. This module implements
an equivalent 64-bit dHash in pure Python so the demo needs zero dependencies.
dHash is deterministic and reproducible, which is exactly Rule R1: a number a
citizen sees must not change when you re-run it.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import asin, cos, radians, sin, sqrt

from saakshi.common.models import Photo, Work

DUP_THRESHOLD = 5        # Hamming <= 5 over 64 bits => near-identical
GEO_TOLERANCE_KM = 2.0   # a completion photo should be AT the work


# ---------- (a) perceptual hashing ------------------------------------------
def dhash(grid: list[list[int]]) -> int:
    """Difference hash: for each row, bit = (pixel < pixel_to_its_right).

    An 8x9 grid yields 8 * 8 = 64 bits. Identical scenes -> identical hash.
    """
    bits = 0
    pos = 0
    for row in grid:
        for c in range(len(row) - 1):
            bits |= (1 if row[c] < row[c + 1] else 0) << pos
            pos += 1
    return bits


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


@dataclass(slots=True)
class DuplicatePair:
    photo_a: str
    photo_b: str
    work_a: str
    work_b: str
    hamming: int
    cross_work: bool
    cross_district: bool
    distance_km: float | None


def find_duplicates(photos: list[Photo], work_index: dict[str, Work],
                    gp_district: dict[int, str],
                    threshold: int = DUP_THRESHOLD) -> list[DuplicatePair]:
    """All near-duplicate pairs. O(n^2) is fine at demo scale; PLAN.md swaps in a
    BK-tree / FAISS-Hamming index for the national corpus."""
    hashes = [(p, dhash(p.grid)) for p in photos]
    out: list[DuplicatePair] = []
    for i in range(len(hashes)):
        pa, ha = hashes[i]
        for j in range(i + 1, len(hashes)):
            pb, hb = hashes[j]
            d = hamming(ha, hb)
            if d > threshold:
                continue
            wa, wb = work_index.get(pa.work_id), work_index.get(pb.work_id)
            cross_work = pa.work_id != pb.work_id
            da = gp_district.get(wa.gp_code) if wa else None
            db = gp_district.get(wb.gp_code) if wb else None
            cross_district = bool(da and db and da != db)
            dist = None
            if wa and wb:
                dist = round(haversine_km(wa.lat, wa.lon, wb.lat, wb.lon), 1)
            out.append(DuplicatePair(pa.photo_id, pb.photo_id, pa.work_id, pb.work_id,
                                     d, cross_work, cross_district, dist))
    out.sort(key=lambda x: (x.hamming, -(x.distance_km or 0)))
    return out


# ---------- (b) geo mismatch ------------------------------------------------
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * asin(sqrt(a))


def geo_mismatches(photos: list[Photo], work_index: dict[str, Work],
                   tolerance_km: float = GEO_TOLERANCE_KM) -> list[tuple[Photo, float]]:
    flags: list[tuple[Photo, float]] = []
    for p in photos:
        if p.lat is None or p.lon is None:
            continue                        # missing EXIF is not evidence of fraud
        w = work_index.get(p.work_id)
        if not w:
            continue
        d = haversine_km(p.lat, p.lon, w.lat, w.lon)
        if d > tolerance_km:
            flags.append((p, round(d, 1)))
    return flags


# ---------- (c) timestamp outside the work window ---------------------------
def timestamp_out_of_window(photos: list[Photo], work_index: dict[str, Work]) -> list[Photo]:
    flags: list[Photo] = []
    for p in photos:
        if p.taken_at is None:
            continue
        w = work_index.get(p.work_id)
        if not w:
            continue
        start = datetime.combine(w.sanction_date, datetime.min.time())
        end = datetime.combine(w.claimed_completion_date or w.sanction_date,
                               datetime.max.time()) + timedelta(days=30)
        if p.taken_at < start or p.taken_at > end:
            flags.append(p)
    return flags


# ---------- (d) impossible device itinerary ---------------------------------
@dataclass(slots=True)
class ItineraryFlag:
    device: str
    start: datetime
    distinct_sites: int
    max_span_km: float
    photo_ids: list[str]


def impossible_itinerary(photos: list[Photo], window_minutes: int = 60,
                         max_sites: int = 3) -> list[ItineraryFlag]:
    """One device geo-tagging attendance at many distinct sites inside one hour.
    Physically impossible; administratively common."""
    by_device: dict[str, list[Photo]] = {}
    for p in photos:
        if p.device and p.taken_at and p.lat is not None:
            by_device.setdefault(p.device, []).append(p)

    flags: list[ItineraryFlag] = []
    for device, rs in by_device.items():
        rs.sort(key=lambda x: x.taken_at)
        best: ItineraryFlag | None = None
        for i, anchor in enumerate(rs):
            window = [x for x in rs[i:]
                      if x.taken_at - anchor.taken_at <= timedelta(minutes=window_minutes)]
            sites = {(round(x.lat, 3), round(x.lon, 3)) for x in window}
            if len(sites) > max_sites and (best is None or len(sites) > best.distinct_sites):
                pts = list(sites)
                span = max((haversine_km(*a, *b) for a in pts for b in pts if a != b),
                           default=0.0)
                best = ItineraryFlag(device, anchor.taken_at, len(sites),
                                     round(span, 1), [x.photo_id for x in window])
        if best is not None:
            flags.append(best)                   # the WORST window for this device
    flags.sort(key=lambda f: f.distinct_sites, reverse=True)
    return flags
