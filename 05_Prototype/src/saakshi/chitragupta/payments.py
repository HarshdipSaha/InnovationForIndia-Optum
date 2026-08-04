"""Detector (2): Payment structure. Fully unsupervised - no labels needed.

(a) threshold splitting   <- the CAG Koppal check-dam fraud
(b) Benford's law         <- weak signal on bill amounts
(c) temporal impossibility <- the CAG "462 instances" fraud

Pure stdlib. The production version (PLAN.md) adds the Payment Heterogeneity
Index (arXiv:2605.12547); the three checks here are the ones that directly
reproduce published CAG findings.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import log10

from saakshi.common.models import Payment, Work

# Statutory tender thresholds (rupees). CONFIGURE PER STATE in production.
THRESHOLDS = [100_000, 250_000, 500_000, 1_000_000, 2_500_000]

# Chi-square critical values, df = 8.
CHI2_CRIT = {0.05: 15.51, 0.01: 20.09, 0.001: 26.12}


# ---------- (a) threshold splitting -----------------------------------------
@dataclass(slots=True)
class SplitGroup:
    gp_code: int
    vendor_id: str | None
    threshold: int
    n_works: int
    combined: float
    work_ids: list[str]


def threshold_splitting(works: list[Work], max_gap_days: int = 60) -> list[SplitGroup]:
    """Two works by the same vendor in the same GP, close in time, each
    individually UNDER a tender threshold but which TOGETHER cross it -- i.e. one
    work split in two to stay under the tendering limit.

    CAG, Koppal (Yelburga taluk): "a check dam split into two smaller works to
    bypass tendering."

    Guards against false positives: each work must be a meaningful fraction of the
    threshold (>= 0.2 t), and the combined value must sit just above it (< 1.6 t),
    which is the signature of a deliberate split rather than unrelated works.
    """
    by: dict[tuple[int, str | None], list[Work]] = {}
    for w in works:
        if w.vendor_id is None:
            continue
        by.setdefault((w.gp_code, w.vendor_id), []).append(w)

    seen: set[tuple] = set()
    out: list[SplitGroup] = []
    for (gp, vid), ws in by.items():
        ws.sort(key=lambda w: w.sanction_date)
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                a, b = ws[i], ws[j]
                if (b.sanction_date - a.sanction_date).days > max_gap_days:
                    break
                combined = a.sanctioned_amount + b.sanctioned_amount
                for t in THRESHOLDS:
                    # each work a meaningful share of the limit, and the pair sits
                    # only just above it -> the fingerprint of a deliberate split.
                    if (a.sanctioned_amount < t and b.sanctioned_amount < t
                            and a.sanctioned_amount >= 0.35 * t
                            and b.sanctioned_amount >= 0.35 * t
                            and t <= combined < 1.25 * t):
                        key = (gp, vid, t, a.work_id, b.work_id)
                        if key in seen:
                            continue
                        seen.add(key)
                        out.append(SplitGroup(gp, vid, t, 2, combined,
                                              [a.work_id, b.work_id]))
                        break
    return out


# ---------- (b) Benford's law -----------------------------------------------
@dataclass(slots=True)
class BenfordResult:
    n: int
    chi2: float
    deviates_at: float | None       # smallest alpha at which it deviates, else None
    observed: list[int]
    expected: list[float]


def benford_first_digit(amounts: list[float]) -> BenfordResult:
    vals = [a for a in amounts if a and a > 0]
    first = [int(str(int(a))[0]) for a in vals]
    observed = [first.count(d) for d in range(1, 10)]
    n = len(first)
    expected = [log10(1 + 1 / d) * n for d in range(1, 10)]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
    deviates_at = None
    for alpha in (0.05, 0.01, 0.001):
        if chi2 > CHI2_CRIT[alpha]:
            deviates_at = alpha
    return BenfordResult(n, round(chi2, 1), deviates_at, observed,
                         [round(e, 1) for e in expected])


# ---------- (c) temporal impossibility --------------------------------------
@dataclass(slots=True)
class TemporalFlag:
    work_id: str
    payment_id: str
    stage: str
    payment_date: date
    completion_date: date
    days_after: int
    amount: float


def temporal_impossibility(payments: list[Payment], works: list[Work]) -> list[TemporalFlag]:
    """The CAG "462 instances" check: stage payments (foundation/lintel/roofing/
    plinth) dated AFTER the work was claimed complete. One date comparison.
    """
    stage_set = {"foundation", "lintel", "roofing", "plinth"}
    windex = {w.work_id: w for w in works}
    flags: list[TemporalFlag] = []
    for p in payments:
        if p.stage not in stage_set:
            continue
        w = windex.get(p.work_id)
        if not w or not w.claimed_completion_date:
            continue
        if p.payment_date > w.claimed_completion_date:
            flags.append(TemporalFlag(
                w.work_id, p.payment_id, p.stage, p.payment_date,
                w.claimed_completion_date,
                (p.payment_date - w.claimed_completion_date).days, p.amount))
    return flags
