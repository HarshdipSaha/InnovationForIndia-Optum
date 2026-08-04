"""GHADI (घड़ी) - the accountability clock (PLAN.md section 10 / idea.md Layer 5).

Assembles the four INDEPENDENT signals into one portable, evidence-linked case
file. Critically (idea.md Layer 1): the signals are NEVER fused into a single
"corruption score" - an IRT validation on Italy's contract database found red
flags are multidimensional and non-superimposable, so a composite index is
statistically unjustified. We present four separate signals + an explicit "what
we do not know" section, and we auto-draft the statutory instruments the citizen
already has the right to file.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from saakshi.common import term
from saakshi.common.models import Work

CONF_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "N/A": 0}


@dataclass(slots=True)
class Signal:
    kind: str                 # PHOTO FORENSIC | SATELLITE | NETWORK | CITIZEN VERIFICATION
    confidence: str           # HIGH | MEDIUM | LOW | N/A
    lines: list[str]
    evidence: list[str] = field(default_factory=list)
    method: str = ""
    caveats: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CaseFile:
    case_id: str
    work: Work
    panchayat_label: str
    lgd_code: int
    signals: list[Signal]
    unknowns: list[str]
    opened: date
    today: date
    rti_deadline_days: int = 30
    cpgrams_deadline_days: int = 21
    cpgrams_ref: str = ""

    # ---- clock ----
    @property
    def rti_deadline(self) -> date:
        return self.opened + timedelta(days=self.rti_deadline_days)

    @property
    def days_elapsed(self) -> int:
        return (self.today - self.opened).days

    @property
    def days_remaining(self) -> int:
        return (self.rti_deadline - self.today).days

    def signal_count(self) -> int:
        return sum(1 for s in self.signals if s.confidence != "N/A")

    # ---- RTI auto-draft (RTI Act 2005, section 6(1)) ----
    def rti_draft(self) -> str:
        w = self.work
        return (
            "To: The Public Information Officer\n"
            f"Subject: Request under section 6(1), Right to Information Act 2005\n\n"
            f"1. In respect of work {w.work_id} (\"{w.work_name}\") in {self.panchayat_label} "
            f"(LGD {self.lgd_code}), sanctioned {term.RUPEE} {w.sanctioned_amount:,.0f} on "
            f"{w.sanction_date:%d %B %Y} under {w.scheme} and marked completed on "
            f"{w.claimed_completion_date:%d %B %Y}, please provide certified copies of:\n"
            "   (a) the measurement book and completion certificate;\n"
            "   (b) all muster rolls and the wage/material payment vouchers;\n"
            "   (c) the geo-tagged completion photographs and their upload logs;\n"
            "   (d) the technical sanction and the third-party quality report, if any.\n"
            "2. Please state the name/designation of the officer who certified completion.\n"
        )


def build_case(*, case_id: str, work: Work, panchayat_label: str, lgd_code: int,
               signals: list[Signal], unknowns: list[str], opened: date,
               today: date, cpgrams_ref: str = "") -> CaseFile:
    signals = sorted(signals, key=lambda s: CONF_ORDER.get(s.confidence, 0), reverse=True)
    return CaseFile(case_id, work, panchayat_label, lgd_code, signals, unknowns,
                    opened, today, cpgrams_ref=cpgrams_ref)


def render(cf: CaseFile, *, color: bool = False) -> str:
    """Render the case file as text.

    ``color=False`` (default) returns plain text - keeps the test suite and any
    piped/captured output clean. The demo passes ``color=term.COLOR`` so the
    live terminal gets styling. ANSI is only ever wrapped around whole,
    already-built strings, so column alignment is computed on plain text first
    and never disturbed by escape codes.
    """
    def paint(fn, s: str) -> str:
        return fn(s) if color else s

    W = 62
    bar = term.HRULE * W
    thin = term.HRULE_THIN * W

    lines: list[str] = [paint(term.saffron_b, bar)]
    lines.append(paint(term.bold, f"CASE {cf.case_id}"))
    lines.append(f"{cf.panchayat_label} {term.BULLET} LGD {cf.lgd_code}")
    lines.append(f"Opened {cf.opened:%d %B %Y} {term.BULLET} Status: "
                 + paint(term.amber, "AWAITING DEPARTMENT RESPONSE"))
    lines.append(paint(term.saffron_b, bar))
    lines.append("")
    w = cf.work
    lines.append(f"{paint(term.dim, 'WORK')}      {w.work_name}")
    lines.append(f"{paint(term.dim, 'SCHEME')}    {w.scheme}")
    lines.append(f"{paint(term.dim, 'SANCTION')}  {term.RUPEE} {w.sanctioned_amount:,.0f} "
                 f"{term.BULLET} {w.sanction_date:%d %B %Y}")
    if w.claimed_completion_date:
        lines.append(f"{paint(term.dim, 'CLAIMED')}   Completed {w.claimed_completion_date:%d %B %Y}")
    lines.append("")
    lines.append(paint(term.saffron,
                       f" {cf.signal_count()} INDEPENDENT SIGNALS ".center(W, term.HRULE_THIN)))

    marks = ["(1)", "(2)", "(3)", "(4)"]
    for i, s in enumerate(cf.signals):
        m = marks[i] if i < len(marks) else "   "
        plain_head = f"{m} {s.kind}"
        head = f"{paint(term.saffron, m)} {paint(term.bold, s.kind)}"
        pad = max(1, 44 - len(plain_head))
        conf = term.confidence(s.confidence) if color else f"confidence {s.confidence}"
        lines.append(f"{head}{' ' * pad}{conf}")
        for ln in s.lines:
            lines.append(f"    {ln}")
        for ln in s.caveats:
            lines.append("    " + paint(term.amber, "!") + f" {ln}")
        if s.method:
            lines.append("    " + paint(term.dim, f"> method: {s.method}"))
        for ev in s.evidence:
            lines.append("    " + paint(term.dim, f"> evidence: {ev}"))
        lines.append("")

    lines.append(paint(term.dim, thin))
    lines.append(paint(term.bold, "WHAT WE DO NOT KNOW"))
    for u in cf.unknowns:
        lines.append(f"    {term.BULLET} {u}")
    lines.append("    " + paint(term.amber, "! This case file is a QUESTION, not a verdict."))
    lines.append(paint(term.dim, thin))
    lines.append(paint(term.bold, "THE CLOCK"))
    lines.append(f"    RTI s.6(1) filed .............. {cf.opened:%d %b %Y}")
    lines.append(f"    Statutory deadline (30 days) .. {cf.rti_deadline:%d %b %Y}")
    lines.append(f"    DAYS ELAPSED: {cf.days_elapsed} {term.BULLET} DAYS REMAINING: {cf.days_remaining}")
    if cf.cpgrams_ref:
        lines.append(f"    CPGRAMS grievance ............. {cf.cpgrams_ref} (21-day deadline)")
    lines.append("    Gram Sabha agenda item ........ queued, next sitting")
    lines.append("    Responsible office ............ [designation only, never a name]")
    lines.append(paint(term.saffron_b, bar))
    return "\n".join(lines)
