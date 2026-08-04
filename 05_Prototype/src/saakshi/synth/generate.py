"""Deterministic synthetic dataset that reconstructs the March 2026 CAG Karnataka
MGNREGA performance audit findings, so the detectors can INDEPENDENTLY re-derive
them (retrospective validation - PLAN.md section 8 / section 11).

IMPORTANT (integrity): this is synthetic data reconstructed to mirror published
CAG findings. It is NOT scraped live-portal data. The production ingest layer
(KOSH) crawls the real public portals; that is out of scope for a zero-network
demo. Everything the demo asserts as "VALIDATED" is a detector rediscovering a
structure that was deliberately seeded to match a published CAG number.

The seeded anchors (see data/ground_truth/cag_karnataka_2026.json):
  * 462 stage payments dated AFTER claimed completion (the CAG "462 instances")
  * a completion photo reused across two works ~61 km apart in different districts
  * a check dam split into two works to dodge the tender threshold (Koppal)
  * a vendor winning 11 of 16 block tenders as the sole bidder
  * one device geo-tagging attendance at 8 sites inside an hour
"""
from __future__ import annotations

import random
from datetime import date, datetime, timedelta

from saakshi.common.models import (
    Bid,
    Dataset,
    Panchayat,
    Payment,
    Photo,
    Tender,
    Vendor,
    Work,
)

SEED = 42
ROWS, COLS = 8, 9   # dHash input grid -> 8 * (9-1) = 64 bits

# Statutory-ish tender threshold used by the split (rupees).
THRESHOLD_5L = 500_000


def _grid(rng: random.Random) -> list[list[int]]:
    return [[rng.randint(0, 255) for _ in range(COLS)] for _ in range(ROWS)]


def _near_dup(grid: list[list[int]], n_pixels: int, rng: random.Random) -> list[list[int]]:
    """Copy a grid and nudge a few interior pixels -> a small Hamming distance."""
    g = [row[:] for row in grid]
    for _ in range(n_pixels):
        r = rng.randint(0, ROWS - 1)
        c = rng.randint(1, COLS - 2)
        g[r][c] = min(255, max(0, g[r][c] + rng.choice([-90, 90])))
    return g


def _jitter(lat: float, lon: float, rng: random.Random, km: float = 0.4) -> tuple[float, float]:
    d = km / 111.0
    return lat + rng.uniform(-d, d), lon + rng.uniform(-d, d)


def generate() -> Dataset:
    rng = random.Random(SEED)
    ds = Dataset()

    # ---- panchayats (LGD-keyed) --------------------------------------------
    kamalapur = Panchayat(226534, "Kamalapur GP", "Kalaburagi", "Kalaburagi", "Karnataka", 17.330, 76.830)
    yelburga = Panchayat(231045, "Yelburga GP", "Yelburga", "Koppal", "Karnataka", 16.778, 76.830)
    sandur = Panchayat(240912, "Sandur GP", "Sandur", "Ballari", "Karnataka", 15.100, 76.550)
    extra = [
        Panchayat(226540 + i, f"GP-{226540 + i}", "Kalaburagi", "Kalaburagi", "Karnataka",
                  17.330 + rng.uniform(-0.4, 0.4), 76.830 + rng.uniform(-0.4, 0.4))
        for i in range(6)
    ]
    ds.panchayats = [kamalapur, yelburga, sandur, *extra]

    # ---- vendors ------------------------------------------------------------
    basava = Vendor("V-04412", "Shri Basava Constructions", "shri basava constructions")
    ds.vendors.append(basava)
    other_vendors = [Vendor(f"V-{5000 + i:05d}", f"Vendor {i} Enterprises", f"vendor {i} enterprises")
                     for i in range(40)]
    ds.vendors.extend(other_vendors)
    vendor_ids = [v.vendor_id for v in other_vendors]

    # Start generated ids high so they never collide with the hand-authored
    # headline work ids (KA-KLB-2026-00412 / KA-KOP-2026-00189).
    work_seq = 20000

    def new_work_id(district_code: str) -> str:
        nonlocal work_seq
        work_seq += 1
        return f"KA-{district_code}-2026-{work_seq:05d}"

    # ---- (1) the headline farm pond + its reused completion photo ----------
    pond_a_id = "KA-KLB-2026-00412"
    pond_b_id = "KA-KOP-2026-00189"
    pond_a = Work(pond_a_id, "Farm pond, survey no. 112/3", "MGNREGA", 420_000.0,
                  date(2026, 3, 12), date(2026, 6, 14), "completed", "farm_pond",
                  kamalapur.gp_code, kamalapur.lat, kamalapur.lon, "V-04412")
    pond_b = Work(pond_b_id, "Farm pond, survey no. 44/1", "MGNREGA", 395_000.0,
                  date(2026, 2, 20), date(2026, 5, 30), "completed", "farm_pond",
                  yelburga.gp_code, yelburga.lat, yelburga.lon, vendor_ids[0])
    ds.works += [pond_a, pond_b]

    shared_scene = _grid(rng)                       # the reused completion photo
    ds.photos.append(Photo("nmms_88213", pond_a_id, [r[:] for r in shared_scene],
                           kamalapur.lat, kamalapur.lon,
                           datetime(2026, 6, 14, 11, 5), "Redmi Note 10", "completion"))
    # the SAME file uploaded against a second work 60+ km away -> Hamming 0
    ds.photos.append(Photo("nmms_71104", pond_b_id, [r[:] for r in shared_scene],
                           yelburga.lat, yelburga.lon,
                           datetime(2026, 5, 30, 9, 40), "Redmi Note 10", "completion"))

    # payments for the pond (no temporal anomaly, so satellite+photo+network carry it)
    ds.payments.append(Payment("PAY-00412-1", pond_a_id, 140_000.0, date(2026, 3, 20), "material"))
    ds.payments.append(Payment("PAY-00412-2", pond_a_id, 180_000.0, date(2026, 5, 2), "wages"))

    # ---- (2) the "462 instances" - stage payments after completion ---------
    n_temporal = 462
    housing_works: list[Work] = []
    for i in range(50):
        wid = new_work_id("KLB")
        comp = date(2026, 3, 1) + timedelta(days=rng.randint(0, 60))
        w = Work(wid, f"PMAY-G house, beneficiary set {i}", "PMAY-G",
                 float(rng.randint(120_000, 145_000)),
                 comp - timedelta(days=rng.randint(120, 200)), comp,
                 "completed", "single_house", kamalapur.gp_code,
                 *_jitter(kamalapur.lat, kamalapur.lon, rng), vendor_ids[i % len(vendor_ids)])
        ds.works.append(w)
        housing_works.append(w)

    stages = ["foundation", "lintel", "roofing", "plinth"]
    for k in range(n_temporal):
        w = housing_works[k % len(housing_works)]
        amt = float(rng.randint(24_000, 27_500))     # ~1.19 crore in aggregate
        pd = w.claimed_completion_date + timedelta(days=rng.randint(7, 95))
        ds.payments.append(Payment(f"PAY-T-{k:04d}", w.work_id, amt, pd, stages[k % 4]))

    # ---- (3) the Koppal check-dam split (threshold evasion) ----------------
    split_a = Work(new_work_id("KOP"), "Check dam (reach A)", "MGNREGA", 240_000.0,
                   date(2026, 4, 3), date(2026, 6, 1), "completed", "check_dam",
                   yelburga.gp_code, *_jitter(yelburga.lat, yelburga.lon, rng), "V-04412")
    split_b = Work(new_work_id("KOP"), "Check dam (reach B)", "MGNREGA", 290_000.0,
                   date(2026, 4, 14), date(2026, 6, 10), "completed", "check_dam",
                   yelburga.gp_code, *_jitter(yelburga.lat, yelburga.lon, rng), "V-04412")
    ds.works += [split_a, split_b]

    # ---- (4) device with an impossible itinerary ---------------------------
    base_t = datetime(2026, 6, 2, 10, 0)
    for s in range(8):
        lat, lon = _jitter(yelburga.lat, yelburga.lon, rng, km=18)
        ds.photos.append(Photo(f"nmms_dev_{s}", split_a.work_id, _grid(rng), lat, lon,
                               base_t + timedelta(minutes=6 * s), "Redmi 9A", "attendance"))

    # ---- broad background works, payments, photos --------------------------
    schemes = ["MGNREGA", "PMAY-G", "SBM-G", "PMGSY"]
    asset_types = ["farm_pond", "check_dam", "road", "single_house", "toilet", "land_levelling"]
    for _ in range(430):
        gp = rng.choice(ds.panchayats)
        wid = new_work_id("KLB")
        sanction = date(2026, 1, 1) + timedelta(days=rng.randint(0, 150))
        completed = rng.random() < 0.75
        comp = sanction + timedelta(days=rng.randint(40, 120)) if completed else None
        w = Work(wid, f"{rng.choice(asset_types)} work", rng.choice(schemes),
                 float(rng.randint(80_000, 900_000)), sanction, comp,
                 "completed" if completed else "ongoing", rng.choice(asset_types),
                 gp.gp_code, *_jitter(gp.lat, gp.lon, rng),
                 rng.choice(vendor_ids))
        ds.works.append(w)
        # a couple of clean payments within the window
        for j in range(rng.randint(1, 3)):
            pd = sanction + timedelta(days=rng.randint(5, 90))
            ds.payments.append(Payment(f"{wid}-P{j}", wid, float(rng.randint(20_000, 300_000)),
                                       pd, rng.choice(["wages", "material"])))
        # one geo-tagged photo, mostly at the site
        if rng.random() < 0.9:
            plat, plon = _jitter(gp.lat, gp.lon, rng, km=1.0 if rng.random() < 0.9 else 40.0)
            # spread times of day so background photos don't cluster into spurious
            # "impossible itinerary" flags; exclude "Redmi 9A" (that device is the
            # injected anomaly and must stand alone).
            taken = (datetime.combine(comp or sanction, datetime.min.time())
                     + timedelta(hours=rng.randint(7, 18), minutes=rng.randint(0, 59)))
            ds.photos.append(Photo(f"ph_{wid}", wid, _grid(rng), plat, plon, taken,
                                   rng.choice(["Redmi Note 10", "Samsung M12", "Vivo Y15", "Oppo A15"]),
                                   "completion" if completed else "progress"))
    # a few extra reused photos in the background so aggregates are non-trivial.
    # Distinct, far-apart timestamps so they don't create spurious itinerary flags.
    for _ in range(12):
        w1, w2 = rng.sample(ds.works, 2)
        scene = _grid(rng)
        t1 = datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 200), hours=rng.randint(6, 18))
        t2 = datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 200), hours=rng.randint(6, 18))
        ds.photos.append(Photo(f"dup_a_{w1.work_id}", w1.work_id, scene, w1.lat, w1.lon,
                               t1, "Oppo A15", "completion"))
        ds.photos.append(Photo(f"dup_b_{w2.work_id}", w2.work_id, _near_dup(scene, 2, rng),
                               w2.lat, w2.lon, t2, "Oppo A15", "completion"))

    # ---- tenders + bids -----------------------------------------------------
    _build_entity(ds, "RDPR::Koppal::Yelburga", yelburga.gp_code, n_tenders=16,
                  n_single_bid=11, primary="V-04412", pool=vendor_ids, rng=rng, asset="check_dam")
    _build_entity(ds, "RDPR::Kalaburagi::Kamalapur", kamalapur.gp_code, n_tenders=23,
                  n_single_bid=12, primary=vendor_ids[3], pool=vendor_ids, rng=rng, asset="farm_pond")
    _build_entity(ds, "PWD::Ballari::Sandur", sandur.gp_code, n_tenders=41,
                  n_single_bid=13, primary=vendor_ids[7], pool=vendor_ids, rng=rng, asset="road")
    # clean background entities
    for i in range(25):
        gp = rng.choice(ds.panchayats)
        n = rng.randint(8, 30)
        _build_entity(ds, f"RDPR::Block{i}::GP{gp.gp_code}", gp.gp_code, n_tenders=n,
                      n_single_bid=rng.randint(0, max(1, n // 6)),
                      primary=rng.choice(vendor_ids), pool=vendor_ids, rng=rng,
                      asset=rng.choice(asset_types))

    return ds


_tender_seq = 0


def _build_entity(ds: Dataset, org_chain: str, gp_code: int, *, n_tenders: int,
                  n_single_bid: int, primary: str, pool: list[str],
                  rng: random.Random, asset: str) -> None:
    global _tender_seq
    multi_winners = rng.sample(pool, k=min(3, len(pool)))
    for i in range(n_tenders):
        _tender_seq += 1
        tid = f"2026_{gp_code}_{_tender_seq:06d}"
        est = float(rng.randint(200_000, 4_000_000))
        single = i < n_single_bid
        if single:
            winner = primary
            n_bidders = 1
            award = round(est * 1.021, 2)          # just above estimate
        else:
            winner = rng.choice(multi_winners)
            n_bidders = rng.randint(2, 4)
            award = round(est * rng.uniform(0.90, 0.98), 2)
        ds.tenders.append(Tender(tid, org_chain, gp_code, est, award, n_bidders, winner,
                                 date(2026, 1, 1) + timedelta(days=rng.randint(0, 180)), asset))
        # bids
        bidders = {winner}
        while len(bidders) < n_bidders:
            bidders.add(rng.choice(pool))
        for b in bidders:
            ds.bids.append(Bid(b, tid, b == winner))
