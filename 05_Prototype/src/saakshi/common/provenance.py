"""Rule R4 (PLAN.md): every fact carries provenance. No exceptions.

We keep this pure-stdlib (no pydantic) so the demo has zero dependencies, but the
contract is identical to the production model in PLAN.md section 4.1: a fact cannot
enter the warehouse without a source portal, URL, fetch time, row locator, a
content hash of the raw bytes parsed, and a parser version.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class Provenance:
    """Attached to every fact. Rule R4. No exceptions."""

    source_portal: str          # "NREGASoft", "CPPP", "AuditOnline"
    source_url: str
    fetched_at: datetime
    row_locator: str            # table+row, or the DOM selector path
    content_sha256: str         # hash of the raw bytes we parsed
    parser_version: str = "1.0"

    @classmethod
    def stamp(
        cls,
        *,
        portal: str,
        url: str,
        raw: bytes,
        locator: str,
        parser_version: str = "1.0",
    ) -> "Provenance":
        return cls(
            source_portal=portal,
            source_url=url,
            fetched_at=datetime.now(timezone.utc),
            row_locator=locator,
            content_sha256=hashlib.sha256(raw).hexdigest(),
            parser_version=parser_version,
        )

    def cite(self) -> str:
        """One-line citation, as it would appear beneath a number in a case file."""
        return f"{self.source_portal} · {self.row_locator} · sha256:{self.content_sha256[:12]}"


@dataclass(frozen=True, slots=True)
class Fact:
    """Nothing enters the warehouse without one of these."""

    payload: dict[str, Any]
    provenance: Provenance
