"""Domain models for the KOSH ledger graph (PLAN.md section 5.1), as plain
dataclasses so the demo stays dependency-free. In production these are Kuzu node
tables; here they are in-memory records with identical fields.

Privacy note (DPDP Act 2023): Beneficiary carries a pseudonymous id and hashed
keys only -- never a name, never an Aadhaar number.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(slots=True)
class Panchayat:
    gp_code: int
    gp_name: str
    block_name: str
    district_name: str
    state_name: str
    lat: float
    lon: float


@dataclass(slots=True)
class Vendor:
    vendor_id: str
    raw_name: str
    canonical_name: str


@dataclass(slots=True)
class Work:
    work_id: str
    work_name: str
    scheme: str
    sanctioned_amount: float
    sanction_date: date
    claimed_completion_date: date | None
    status: str                 # sanctioned | ongoing | completed
    asset_type: str             # farm_pond | check_dam | single_house | road | toilet ...
    gp_code: int
    lat: float
    lon: float
    vendor_id: str | None = None


@dataclass(slots=True)
class Payment:
    payment_id: str
    work_id: str
    amount: float
    payment_date: date
    stage: str                  # foundation | lintel | roofing | plinth | wages | material


@dataclass(slots=True)
class Photo:
    photo_id: str
    work_id: str
    grid: list[list[int]]       # 8 rows x 9 cols greyscale (0-255); dHash input
    lat: float | None
    lon: float | None
    taken_at: datetime | None
    device: str | None
    claimed_stage: str


@dataclass(slots=True)
class Tender:
    tender_id: str
    org_chain: str              # e.g. "RDPR::Koppal::Yelburga"
    gp_code: int
    estimate_value: float
    award_value: float
    num_bidders: int
    winner_id: str
    award_date: date
    asset_type: str


@dataclass(slots=True)
class Bid:
    vendor_id: str
    tender_id: str
    is_winner: bool


@dataclass(slots=True)
class Dataset:
    panchayats: list[Panchayat] = field(default_factory=list)
    vendors: list[Vendor] = field(default_factory=list)
    works: list[Work] = field(default_factory=list)
    payments: list[Payment] = field(default_factory=list)
    photos: list[Photo] = field(default_factory=list)
    tenders: list[Tender] = field(default_factory=list)
    bids: list[Bid] = field(default_factory=list)

    # ---- convenience lookups ----
    def work(self, work_id: str) -> Work | None:
        return next((w for w in self.works if w.work_id == work_id), None)

    def panchayat(self, gp_code: int) -> Panchayat | None:
        return next((p for p in self.panchayats if p.gp_code == gp_code), None)

    def vendor(self, vendor_id: str) -> Vendor | None:
        return next((v for v in self.vendors if v.vendor_id == vendor_id), None)

    def photos_for(self, work_id: str) -> list[Photo]:
        return [ph for ph in self.photos if ph.work_id == work_id]
