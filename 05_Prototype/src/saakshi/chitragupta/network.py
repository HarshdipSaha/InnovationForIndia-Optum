"""Detector (3): Network / procurement red flags.

Computes the standard World Bank / DIGIWHIST indicators that NO INDIAN BODY
PUBLISHES (RESEARCH.md A7.3):
  * single-bid rate                (the headline corruption indicator worldwide)
  * repeat-winner concentration    (Herfindahl-Hirschman Index)
  * award-vs-estimate premium
  * sole-bidder wins per vendor     (identifies the Basava-style pattern)

Rule R3 (PLAN.md): a LightGBM baseline on these graph-derived features ships
first; a GAT must beat it to be used. The demo computes the deterministic red
flags (which are what a citizen sees); the ML score lives in the internal triage
queue only.
"""
from __future__ import annotations

from dataclasses import dataclass

from saakshi.common.models import Bid, Tender


@dataclass(slots=True)
class EntityRedFlags:
    org_chain: str
    n_tenders: int
    n_single_bid: int
    single_bid_rate: float
    mean_award_premium: float       # (award-estimate)/estimate, averaged
    winner_diversity: float         # distinct winners / tenders
    hhi: float                      # repeat-winner concentration (0..1)


def red_flags_by_entity(tenders: list[Tender], min_tenders: int = 10) -> list[EntityRedFlags]:
    by_org: dict[str, list[Tender]] = {}
    for t in tenders:
        by_org.setdefault(t.org_chain, []).append(t)

    out: list[EntityRedFlags] = []
    for org, ts in by_org.items():
        if len(ts) < min_tenders:
            continue
        n = len(ts)
        n_single = sum(1 for t in ts if t.num_bidders == 1)
        premiums = [(t.award_value - t.estimate_value) / t.estimate_value
                    for t in ts if t.estimate_value > 0]
        winners = [t.winner_id for t in ts]
        distinct = len(set(winners))
        shares = [winners.count(w) / n for w in set(winners)]
        hhi = sum(s * s for s in shares)
        out.append(EntityRedFlags(
            org, n, n_single, round(n_single / n, 3),
            round(sum(premiums) / len(premiums), 4) if premiums else 0.0,
            round(distinct / n, 3), round(hhi, 3)))
    out.sort(key=lambda e: e.single_bid_rate, reverse=True)
    return out


def national_single_bid_rate(tenders: list[Tender]) -> tuple[float, int, int]:
    n = len(tenders)
    single = sum(1 for t in tenders if t.num_bidders == 1)
    return (round(single / n, 4) if n else 0.0, single, n)


@dataclass(slots=True)
class VendorFlag:
    vendor_id: str
    tenders_won: int
    sole_bidder_wins: int
    mean_premium: float


def sole_bidder_vendors(tenders: list[Tender], bids: list[Bid],
                        min_sole_wins: int = 5) -> list[VendorFlag]:
    """Vendors that repeatedly win as the ONLY bidder - the Basava pattern."""
    tindex = {t.tender_id: t for t in tenders}
    won: dict[str, list[Tender]] = {}
    for b in bids:
        if b.is_winner and b.tender_id in tindex:
            won.setdefault(b.vendor_id, []).append(tindex[b.tender_id])
    out: list[VendorFlag] = []
    for vid, ts in won.items():
        sole = sum(1 for t in ts if t.num_bidders == 1)
        if sole < min_sole_wins:
            continue
        premiums = [(t.award_value - t.estimate_value) / t.estimate_value
                    for t in ts if t.estimate_value > 0]
        out.append(VendorFlag(vid, len(ts), sole,
                              round(sum(premiums) / len(premiums), 4) if premiums else 0.0))
    out.sort(key=lambda v: v.sole_bidder_wins, reverse=True)
    return out
