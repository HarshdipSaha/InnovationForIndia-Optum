# PLAN.md — Building SAAKSHI

**Companion to:** `idea.md` (the idea) and `RESEARCH.md` (the evidence)
**Target:** TechGig × Optum — *Inclusive Innovation for Bharat*, Theme 05 (GovTech & Public Service Delivery)
**License:** MIT (hackathon requirement — drives every dependency choice below)

> This document is the build. Every phase states **what you do**, **the code**, **what the output looks like**, and **how you know it worked**.

---

## Table of Contents

- [0. Read this first — the build philosophy](#0-read-this-first--the-build-philosophy)
- [1. Tech stack, with justification](#1-tech-stack-with-justification)
- [2. Repository structure](#2-repository-structure)
- [3. Phase 0 — Environment setup](#3-phase-0--environment-setup)
- [4. Phase 1 — KOSH: ingest](#4-phase-1--kosh-ingest)
- [5. Phase 2 — KOSH: the graph](#5-phase-2--kosh-the-graph)
- [6. Phase 3 — CHITRAGUPTA: the four detectors](#6-phase-3--chitragupta-the-four-detectors)
- [7. Phase 4 — NAAM-MILAN: Indic entity resolution](#7-phase-4--naam-milan-indic-entity-resolution)
- [8. Phase 5 — VAANI: the voice layer](#8-phase-5--vaani-the-voice-layer)
- [9. Phase 6 — PRAMAAN: citizen verification](#9-phase-6--pramaan-citizen-verification)
- [10. Phase 7 — GHADI: the accountability clock](#10-phase-7--ghadi-the-accountability-clock)
- [11. Phase 8 — The killer demo](#11-phase-8--the-killer-demo)
- [12. OUTPUT SPECIFICATIONS — what everything looks like](#12-output-specifications--what-everything-looks-like)
- [13. Testing strategy](#13-testing-strategy)
- [14. Build order and timeline](#14-build-order-and-timeline)
- [15. Submission deliverables checklist](#15-submission-deliverables-checklist)
- [16. Known risks and mitigations](#16-known-risks-and-mitigations)

---

## 0. Read this first — the build philosophy

Five rules. Breaking any of them makes the system worse, not better.

| # | Rule | Why |
|---|---|---|
| **R1** | **Deterministic path for anything a citizen sees.** Perceptual hashes, date comparisons, `GROUP BY`s and parameterised queries only. ML scores live in the **internal triage queue**, never as the sole basis of a citizen-facing claim | Financial ML pipelines are **not deterministic across re-runs** (arXiv:2605.23955). A number that changes when you re-run it cannot survive a legal challenge |
| **R2** | **No LLM ever writes a query.** Intent classification + slot extraction + translation. Nothing else | 54–69% execution accuracy for strong commercial models on provenance-aware graphs; **6–19% for 7B open models, which never abstain** (arXiv:2607.25243) |
| **R3** | **Boring baseline first, fancy model as challenger.** LightGBM on graph features before any GNN | **GADBench: tree ensembles with simple neighborhood aggregation outperform the latest task-specific GNNs** across 29 models × 10 datasets (arXiv:2306.12251) |
| **R4** | **Every number carries provenance.** Source portal + fetch timestamp + row ID + document URL | Citation validity is a first-class metric (arXiv:2604.19755: 0.98 citation validity, 0.88 evidence support) |
| **R5** | **Ship the honest limit alongside the capability.** Every detector emits its own confidence *and its own failure mode* | Overclaiming is how you lose a technical judge. And it's how you deploy something that hurts people |

**Build order is deliberately inverted from the layer numbering.** Build the *demo-critical* path first (photo forensics + satellite + case file), because that is what wins the room. Voice and entity resolution come second. See §14.

---

## 1. Tech stack, with justification

| Concern | Choice | Why this and not the obvious alternative |
|---|---|---|
| Language | **Python 3.11+** | Ecosystem. Non-negotiable |
| Package manager | **uv** | 10–100× faster than pip; lockfile; a judge running your repo should not wait |
| Tabular store | **DuckDB** (MIT) | Embedded, columnar, reads Parquet/CSV natively, zero infra. **A judge can clone and run.** Postgres needs a server |
| Graph store | **KùzuDB** (MIT) | **Embedded** property graph with Cypher. Neo4j needs a server and its community edition licensing is a headache for an MIT deliverable |
| Dataframes | **Polars** | Lazy, fast, good CSV/Parquet. pandas where a library demands it |
| HTTP | **httpx** | HTTP/2, async, proper cookie jar — **required for the NREGASoft session problem** |
| Browser automation | **Playwright** | NREGASoft is ASP.NET postback forms. requests cannot drive `__VIEWSTATE`. Playwright can |
| HTML parsing | **selectolax** | ~10× faster than BeautifulSoup on large government tables |
| Perceptual hashing | **imagehash** + **Pillow** | pHash/dHash. This is a solved problem — do not reinvent |
| EXIF | **exifread** | Raw EXIF including GPS IFD |
| Satellite | **pystac-client** + **rasterio** + **Element84 Earth Search** | **Free Sentinel-2 L2A COGs, no auth, no signup.** Google Earth Engine needs an account and has non-commercial terms — bad for an MIT deliverable |
| ML | **LightGBM** + **scikit-learn** | R3. LightGBM is the GADBench-endorsed baseline |
| PU learning | **pulearn** or hand-rolled Elkan-Noto | The literature's answer to no-confirmed-negatives (arXiv:2512.19491) |
| Entity resolution | **splink** (MIT) + **rapidfuzz** + **BlockingPy** | Splink gives Fellegi-Sunter with EM and **calibrated posteriors** — exactly the d-blink property we need |
| Transliteration | **IndicXlit** (Aksharantar) via **ai4bharat-transliteration** | **26M pairs, 21 languages, 12 scripts** (arXiv:2205.03018) |
| Indic MT | **IndicTrans2** | **All 22 scheduled languages, open weights, permissive** (arXiv:2305.16307) |
| ASR / TTS | **Bhashini API** (primary) + **IndicConformer** (fallback) | Bhashini is **already deployed across eGramSwaraj, LGD, AuditOnline, Meri Panchayat.** Reuse government DPI — it's a scoring point, not just convenience |
| OCR | **PaddleOCR 3.0** (Apache-2.0) + **Qwen3-VL-8B** | Qwen3-VL-8B scored **75.2 chrF++ on real Devanagari scans** — the best *open* result, and runs on one 24 GB GPU (arXiv:2606.29213) |
| Image forensics | **DINOv3 frozen + LoRA head** | **+17.0 pixel-F1 with 9.1M trainable params** (arXiv:2604.16083) |
| Telephony | **Exotel** (primary) / **Twilio** (dev) | Exotel is Indian, has toll-free + IVR + regional presence. Twilio for local dev because its test credentials are frictionless |
| API | **FastAPI** + **Pydantic v2** | Typed contracts. Pydantic models *are* the output spec |
| UI | **Jinja2 + HTMX + Leaflet** | No build step, no `node_modules`, works offline. A judge opens one URL. React is a liability here |
| ZK | **circomlib / snarkjs** (PoC) | zkSNARK set-membership per DARTIC (arXiv:2605.18146). **PoC-only in hackathon scope — see §9.3** |
| Scheduling | **APScheduler** | In-process. Airflow is infra you don't need |
| Testing | **pytest** + **pytest-vcr** | VCR cassettes so scraper tests run offline in CI |

> **The through-line:** every choice is embedded, MIT/Apache-licensed, and runnable from `git clone && uv sync && make demo`. **A judge who cannot run your prototype scores your prototype as a mockup.**

---

## 2. Repository structure

```
saakshi/
├── README.md                      # 60-second quickstart + the demo GIF
├── LICENSE                        # MIT — hackathon requirement
├── pyproject.toml
├── Makefile                       # make ingest / detect / demo / serve
├── .env.example
│
├── data/
│   ├── raw/                       # immutable landing zone, never edited
│   │   ├── lgd/                   # Local Government Directory bulk export
│   │   ├── nrega/                 # NREGASoft crawl output
│   │   ├── cppp/                  # tender + bid award HTML
│   │   ├── egramswaraj/
│   │   ├── auditonline/
│   │   ├── cpgrams/
│   │   ├── photos/                # NMMS / AwaasSoft geo-tagged images
│   │   └── sentinel/              # cached Sentinel-2 COG windows
│   ├── warehouse.duckdb           # tabular facts
│   ├── kosh.kuzu/                 # the graph
│   └── ground_truth/
│       └── cag_karnataka_2026.yaml   # ⭐ the validation set
│
├── src/saakshi/
│   ├── ingest/
│   │   ├── base.py                # Connector ABC + provenance stamping
│   │   ├── lgd.py                 # the join key. Build this FIRST
│   │   ├── nrega.py               # ⚠ session-aware. The hard one
│   │   ├── cppp.py                # tenders + bid awards
│   │   ├── egramswaraj.py
│   │   ├── auditonline.py
│   │   ├── cpgrams.py
│   │   ├── dbt.py
│   │   └── impds.py
│   │
│   ├── kosh/
│   │   ├── schema.py              # Kuzu DDL
│   │   ├── build.py               # DuckDB → Kuzu
│   │   └── queries/               # ⭐ ~40 parameterised queries. THE contract
│   │       ├── q001_panchayat_year_summary.cypher
│   │       ├── q002_work_detail.cypher
│   │       └── ...
│   │
│   ├── chitragupta/
│   │   ├── network.py             # ① collusion graph + red flags
│   │   ├── payments.py            # ② threshold split, Benford, PHI, temporal
│   │   ├── photos.py              # ③ pHash, EXIF, device cluster, writer retrieval
│   │   ├── satellite.py           # ④ Sentinel-2 bi-temporal change
│   │   └── fuse.py                # ⚠ does NOT fuse into one score. Assembles evidence
│   │
│   ├── naammilan/
│   │   ├── canonicalize.py        # IndicXlit + phonetic keys
│   │   ├── block.py               # ANN blocking
│   │   └── resolve.py             # splink → calibrated posteriors
│   │
│   ├── vaani/
│   │   ├── ivr.py                 # telephony webhooks (state machine)
│   │   ├── intent.py              # ⭐ router. NEVER text-to-SQL
│   │   ├── slots.py               # slot extraction + confirmation loops
│   │   ├── asr.py                 # Bhashini + diarization + script guard
│   │   └── nlg.py                 # templated answers → IndicTrans2
│   │
│   ├── pramaan/
│   │   ├── attest.py              # device-signed capture verification
│   │   ├── anon.py                # zkSNARK set-membership (PoC)
│   │   ├── truth.py               # truth discovery over reports
│   │   └── labels.py              # ⭐ verified reports → PU labels
│   │
│   ├── ghadi/
│   │   ├── casefile.py            # the case file model
│   │   ├── rti.py                 # RTI §6(1) draft generator
│   │   ├── cpgrams.py             # grievance draft
│   │   └── clock.py               # deadlines + recovery ledger
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── routes_public.py
│   │   ├── routes_ivr.py
│   │   └── templates/
│   │
│   └── common/
│       ├── provenance.py          # ⭐ R4 enforcement
│       ├── lgd_codes.py
│       └── config.py
│
├── notebooks/
│   └── 01_cag_retrospective.ipynb # ⭐ THE DEMO
│
├── tests/
└── docs/
    ├── architecture.excalidraw
    └── DATA_SOURCES.md
```

---

## 3. Phase 0 — Environment setup

```powershell
# Windows PowerShell
mkdir saakshi; cd saakshi
git init
uv init --python 3.11

uv add duckdb kuzu polars httpx[http2] selectolax playwright `
       imagehash pillow exifread `
       pystac-client rasterio shapely pyproj `
       lightgbm scikit-learn `
       splink rapidfuzz `
       fastapi "uvicorn[standard]" jinja2 python-multipart `
       pydantic pydantic-settings apscheduler `
       structlog rich typer

uv add --dev pytest pytest-vcr pytest-cov ruff mypy

uv run playwright install chromium
```

`.env.example`:

```ini
# --- Telephony (Exotel prod / Twilio dev) ---
TELEPHONY_PROVIDER=twilio
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
EXOTEL_SID=
EXOTEL_TOKEN=
SAAKSHI_TOLLFREE=

# --- Bhashini (ASR / TTS / MT) ---
BHASHINI_USER_ID=
BHASHINI_ULCA_API_KEY=
BHASHINI_PIPELINE_ID=

# --- Satellite: Element84 Earth Search needs NO auth ---
STAC_API_URL=https://earth-search.aws.element84.com/v1

# --- Scraping etiquette ---
CRAWL_DELAY_SECONDS=2
USER_AGENT=SAAKSHI/0.1 (research; +https://github.com/<you>/saakshi)

# --- Storage ---
DUCKDB_PATH=data/warehouse.duckdb
KUZU_PATH=data/kosh.kuzu
```

> ### ⚠️ Scraping ethics — do this, and put it in the README
>
> Every source in this project is **published by the Government of India for public consumption**. Even so:
> 1. Respect `robots.txt`. Check it per portal, log the check.
> 2. **Rate-limit to 1 request / 2 seconds.** These are public servers funded by taxpayers, including the ones you're helping.
> 3. Identify yourself honestly in the `User-Agent`, with a contact URL.
> 4. **Cache aggressively.** Never re-fetch what you already have.
> 5. Never attempt to access anything behind authentication. PFMS is login-gated — **that means it is out of scope, full stop.**
>
> **This paragraph belongs in your README.** A judge who sees it reads "responsible engineer." A judge who doesn't wonder what else you cut corners on.

---

## 4. Phase 1 — KOSH: ingest

### 4.1 The provenance contract (build this before any connector)

Rule R4 is enforced by making it structurally impossible to insert a fact without provenance.

```python
# src/saakshi/common/provenance.py
from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field, HttpUrl


class Provenance(BaseModel):
    """Attached to every fact. Rule R4. No exceptions."""
    source_portal: str          # "NREGASoft", "CPPP", "AuditOnline"
    source_url: HttpUrl
    fetched_at: datetime
    row_locator: str            # table+row, or the DOM selector path
    content_sha256: str         # hash of the raw bytes we parsed
    parser_version: str

    @classmethod
    def stamp(cls, *, portal: str, url: str, raw: bytes,
              locator: str, parser_version: str = "1.0") -> "Provenance":
        return cls(
            source_portal=portal,
            source_url=url,
            fetched_at=datetime.now(timezone.utc),
            row_locator=locator,
            content_sha256=hashlib.sha256(raw).hexdigest(),
            parser_version=parser_version,
        )


class Fact(BaseModel):
    """Nothing enters the warehouse without one of these."""
    payload: dict[str, Any]
    provenance: Provenance
```

### 4.2 LGD — build this first, everything depends on it

The Local Government Directory is the join key. Cabinet Secretariat mandated LGD codes across all e-Government applications on **4 November 2016**. **Without this, there is no project.**

```python
# src/saakshi/ingest/lgd.py
"""
Local Government Directory — the spine.

36 States/UTs · 784 districts · 7,092 sub-districts · 7,323 blocks
677,042 villages (657,769 inhabited) · 255,297 gram panchayats

Bulk export: https://lgdirectory.gov.in/  → "Download Directory"
API:         https://dev.napix.gov.in/nic/lgd/

Download the bulk CSVs manually ONCE into data/raw/lgd/.
Do not crawl what is offered as a download.
"""
import duckdb, polars as pl
from pathlib import Path

RAW = Path("data/raw/lgd")


def load_lgd(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("""
        CREATE OR REPLACE TABLE lgd_hierarchy AS
        SELECT
            CAST(state_code    AS INTEGER) AS state_code,
            state_name_english             AS state_name,
            CAST(district_code AS INTEGER) AS district_code,
            district_name_english          AS district_name,
            CAST(block_code    AS INTEGER) AS block_code,
            block_name_english             AS block_name,
            CAST(gp_code       AS INTEGER) AS gp_code,
            gp_name_english                AS gp_name,
            CAST(village_code  AS INTEGER) AS village_code,
            village_name_english           AS village_name
        FROM read_csv_auto(?, header=true, ignore_errors=true)
    """, [str(RAW / "lgd_villages.csv")])

    # gp_code is the join key for everything downstream.
    con.execute("CREATE INDEX IF NOT EXISTS idx_lgd_gp ON lgd_hierarchy(gp_code)")

    n = con.execute("SELECT COUNT(DISTINCT gp_code) FROM lgd_hierarchy").fetchone()[0]
    print(f"LGD loaded: {n:,} gram panchayats")
    # Expect ≈ 255,297. If you get 200, you downloaded one state.
```

**Expected output:**
```
LGD loaded: 255,297 gram panchayats
```

### 4.3 ⚠️ NREGASoft — the hard one

**The problem, verified during research:** `mnregaweb4.nic.in` **returns "URL Tampered" on direct deep-links.** NIC enforces referrer/session validation, and the reports are ASP.NET postback forms driven by `__VIEWSTATE` / `__EVENTVALIDATION`.

**The proof it's solvable:** LibTech India crawled **31.36 million transactions across 10 states** this way.

**Two strategies. Use both.**

```python
# src/saakshi/ingest/nrega.py
"""
NREGASoft — richest data in Indian GovTech, least link-friendly.

⚠ Deep-links are rejected with "URL Tampered".
   You MUST walk the navigation from MISreport4.aspx so the server
   sees a valid Referer and an intact session cookie.

Strategy A (httpx): keep one AsyncClient, prime the session on the
   landing page, then POST with a correct Referer. Fast. Fragile.
Strategy B (Playwright): drive a real browser through the postback
   form. Slow. Robust. Use for the reports Strategy A cannot reach —
   notably R 9.2.6 Financial Misappropriation Recovery.
"""
import asyncio, httpx
from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright

BASE   = "https://mnregaweb4.nic.in/netnrega"
LANDING = f"{BASE}/MISreport4.aspx"
UA = "SAAKSHI/0.1 (research; +https://github.com/<you>/saakshi)"


# ---------- Strategy A ----------
class NregaSession:
    def __init__(self, delay: float = 2.0):
        self._delay = delay
        self._client = httpx.AsyncClient(
            http2=True, timeout=60.0, follow_redirects=True,
            headers={"User-Agent": UA,
                     "Accept-Language": "en-IN,en;q=0.9"},
        )

    async def __aenter__(self):
        # Prime the session. This sets ASP.NET_SessionId and is what
        # makes the server stop saying "URL Tampered".
        r = await self._client.get(LANDING)
        r.raise_for_status()
        self._viewstate = self._hidden(r.text)
        return self

    async def __aexit__(self, *exc):
        await self._client.aclose()

    @staticmethod
    def _hidden(html: str) -> dict[str, str]:
        """ASP.NET hidden fields must be echoed back on every postback."""
        tree = HTMLParser(html)
        out = {}
        for name in ("__VIEWSTATE", "__VIEWSTATEGENERATOR",
                     "__EVENTVALIDATION", "__EVENTTARGET", "__EVENTARGUMENT"):
            node = tree.css_first(f'input[name="{name}"]')
            out[name] = node.attributes.get("value", "") if node else ""
        return out

    async def report(self, path: str, params: dict[str, str]) -> str:
        """Fetch a report WITH a Referer so the tamper check passes."""
        await asyncio.sleep(self._delay)
        url = f"{BASE}/{path}"
        r = await self._client.get(
            url, params=params,
            headers={"Referer": LANDING},   # ← the critical header
        )
        if "URL Tampered" in r.text:
            raise RuntimeError(
                f"Tamper check failed for {path}. "
                "Session expired or navigation path invalid — "
                "fall back to Strategy B (Playwright)."
            )
        return r.text


# ---------- Strategy B ----------
async def fetch_misappropriation_report(fin_year: str = "2025-2026") -> str:
    """
    R 9.2.6 Financial Misappropriation Recovery Report.

    This is THE report — the government's own detected-vs-recovered
    numbers. It is not reachable by URL. Drive the browser.
    """
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=UA)

        await page.goto(LANDING, wait_until="networkidle")
        await page.get_by_role("link", name="Social Audit").click()
        await page.wait_for_load_state("networkidle")
        await page.get_by_role(
            "link", name="Financial Misappropriation").click()
        await page.wait_for_load_state("networkidle")
        await page.select_option("select#ddl_fin_year", fin_year)
        await page.wait_for_load_state("networkidle")

        html = await page.content()
        await browser.close()
        return html
```

**Expected output — parsed R 9.2.6:**
```
state           detected_cr   recovered_cr   recovery_pct
------------------------------------------------------------
Tamil Nadu            26.57           1.33           5.0%
Maharashtra           31.02           4.11          13.3%
Karnataka             44.18           3.90           8.8%
...
NATIONAL             110.89          14.02          12.6%   ← the headline
```

> **This table is your opening slide.** It is the government's own number, scraped from the government's own portal, live. Under 13% recovered.

### 4.4 CPPP — tenders and bid awards

This is where India's first single-bid rate comes from.

```python
# src/saakshi/ingest/cppp.py
"""
Central Public Procurement Portal.
97,884 active tenders. Bid awards PUBLIC at /resultoftendersnew.

⭐ This connector produces India's first published single-bid rate.
"""
import httpx, polars as pl
from selectolax.parser import HTMLParser
from saakshi.common.provenance import Provenance

CPPP = "https://eprocure.gov.in/cppp"
AWARDS = f"{CPPP}/resultoftendersnew"


def parse_awards(html: str, url: str) -> list[dict]:
    tree = HTMLParser(html)
    rows = []
    for tr in tree.css("table.list_table tr")[1:]:
        td = [c.text(strip=True) for c in tr.css("td")]
        if len(td) < 8:
            continue
        rows.append({
            "tender_id":      td[1],
            "org_chain":      td[2],
            "tender_title":   td[3],
            "estimate_value": _money(td[4]),
            "award_value":    _money(td[5]),
            "num_bidders":    _int(td[6]),      # ← the money column
            "winner_name":    td[7],
            "award_date":     td[8] if len(td) > 8 else None,
            "_prov": Provenance.stamp(
                portal="CPPP", url=url,
                raw=html.encode(), locator=f"awards#{td[1]}").model_dump(),
        })
    return rows


def _money(s: str) -> float | None:
    s = s.replace(",", "").replace("₹", "").strip()
    try:    return float(s)
    except ValueError: return None


def _int(s: str) -> int | None:
    try:    return int(s.strip())
    except ValueError: return None
```

### 4.5 AuditOnline — the 0 ATRs

```python
# src/saakshi/ingest/auditonline.py
"""
AuditOnline (Ministry of Panchayati Raj).

FY2025-26 national counters, verified 29 Jul 2026:
  auditees        262,202  (255,402 gram panchayats)
  observations     62,745
  audit reports     5,657  (2.2%)
  settlements           0  ← 
  action taken          0  ← the entire justification for Layer 5

Citizen Section exposes PDF + Excel downloads. No login.
"""
```

### 4.6 CPGRAMS dashboard

```python
# src/saakshi/ingest/cpgrams.py
"""
Public HTML table, date-range selectable, no login.
https://pgportal.gov.in/darpgdashboard

Columns: department | received | disposed | disposal% | pending
         | pending>30d | pending>60d

Rural Development 81.13% · Panchayati Raj 87.11%
vs Financial Services 96.92%.
⇒ The departments serving the poorest perform worst.
"""
```

---

## 5. Phase 2 — KOSH: the graph

### 5.1 Schema

```python
# src/saakshi/kosh/schema.py
DDL = [
# ---------------- NODES ----------------
"""CREATE NODE TABLE IF NOT EXISTS Panchayat(
     gp_code INT64, gp_name STRING, block_name STRING,
     district_name STRING, state_name STRING,
     lat DOUBLE, lon DOUBLE,
     PRIMARY KEY (gp_code))""",

"""CREATE NODE TABLE IF NOT EXISTS Work(
     work_id STRING, work_name STRING, scheme STRING,
     sanctioned_amount DOUBLE, sanction_date DATE,
     claimed_completion_date DATE, status STRING,
     asset_type STRING,          -- pond|road|house|toilet|checkdam|...
     lat DOUBLE, lon DOUBLE,
     satellite_verifiable BOOLEAN,   -- ⭐ set by asset_type. See §6.4
     PRIMARY KEY (work_id))""",

"""CREATE NODE TABLE IF NOT EXISTS Contract(
     tender_id STRING, title STRING, org_chain STRING,
     estimate_value DOUBLE, award_value DOUBLE,
     num_bidders INT64, award_date DATE,
     PRIMARY KEY (tender_id))""",

"""CREATE NODE TABLE IF NOT EXISTS Vendor(
     vendor_id STRING, raw_name STRING, canonical_name STRING,
     PRIMARY KEY (vendor_id))""",

"""CREATE NODE TABLE IF NOT EXISTS Payment(
     payment_id STRING, amount DOUBLE, payment_date DATE,
     stage STRING, fto_no STRING,
     PRIMARY KEY (payment_id))""",

"""CREATE NODE TABLE IF NOT EXISTS Photo(
     photo_id STRING, file_path STRING,
     phash STRING, dhash STRING,
     exif_lat DOUBLE, exif_lon DOUBLE, exif_ts TIMESTAMP,
     device_model STRING, claimed_stage STRING,
     PRIMARY KEY (photo_id))""",

# NEVER a name. NEVER an Aadhaar number.
"""CREATE NODE TABLE IF NOT EXISTS Beneficiary(
     pseudo_id STRING, name_hash STRING, phonetic_key STRING,
     gp_code INT64,
     PRIMARY KEY (pseudo_id))""",

"""CREATE NODE TABLE IF NOT EXISTS AuditObservation(
     obs_id STRING, obs_text STRING, obs_date DATE,
     amount_involved DOUBLE, settled BOOLEAN, atr_filed BOOLEAN,
     PRIMARY KEY (obs_id))""",

"""CREATE NODE TABLE IF NOT EXISTS CitizenReport(
     report_id STRING, question_id STRING,
     answer STRING,                 -- yes|no|unsure
     received_at TIMESTAMP,
     anon_commitment STRING,        -- zkSNARK commitment. NEVER a phone number
     PRIMARY KEY (report_id))""",

"""CREATE NODE TABLE IF NOT EXISTS SatelliteObservation(
     obs_id STRING, work_id STRING,
     before_date DATE, after_date DATE,
     ndwi_delta DOUBLE, ndvi_delta DOUBLE, ndbi_delta DOUBLE,
     change_detected BOOLEAN, confidence STRING,   -- HIGH|LOW|N/A
     scene_before STRING, scene_after STRING,
     PRIMARY KEY (obs_id))""",

# ---------------- EDGES ----------------
"CREATE REL TABLE IF NOT EXISTS LOCATED_IN(FROM Work TO Panchayat)",
"CREATE REL TABLE IF NOT EXISTS AWARDED_TO(FROM Contract TO Vendor)",
"CREATE REL TABLE IF NOT EXISTS BID_ON(FROM Vendor TO Contract, is_winner BOOLEAN)",
"CREATE REL TABLE IF NOT EXISTS FUNDS(FROM Contract TO Work)",
"CREATE REL TABLE IF NOT EXISTS PAID_FOR(FROM Payment TO Work)",
"CREATE REL TABLE IF NOT EXISTS EVIDENCES(FROM Photo TO Work)",
"CREATE REL TABLE IF NOT EXISTS DUPLICATE_OF(FROM Photo TO Photo, hamming INT64)",
"CREATE REL TABLE IF NOT EXISTS BENEFITS(FROM Work TO Beneficiary)",
"CREATE REL TABLE IF NOT EXISTS SAME_AS(FROM Beneficiary TO Beneficiary, posterior DOUBLE)",
"CREATE REL TABLE IF NOT EXISTS OBSERVED_ON(FROM AuditObservation TO Work)",
"CREATE REL TABLE IF NOT EXISTS REPORTS_ON(FROM CitizenReport TO Work)",
"CREATE REL TABLE IF NOT EXISTS IMAGES(FROM SatelliteObservation TO Work)",
]
```

### 5.2 ⭐ The parameterised query library — the R2 contract

**This directory is the single most important design artefact in the repo.** It is the *only* way anything reaches the database.

```cypher
// src/saakshi/kosh/queries/q001_panchayat_year_summary.cypher
// INTENT: panchayat_year_summary
// SLOTS:  $gp_code (INT64), $fy_start (DATE), $fy_end (DATE)
// ANSWERS: "What did my panchayat receive this year?"
MATCH (p:Panchayat {gp_code: $gp_code})<-[:LOCATED_IN]-(w:Work)
WHERE w.sanction_date >= $fy_start AND w.sanction_date <= $fy_end
RETURN p.gp_name                                        AS panchayat,
       count(w)                                         AS total_works,
       sum(w.sanctioned_amount)                         AS total_sanctioned,
       count(CASE WHEN w.status = 'completed' THEN 1 END) AS completed,
       collect(DISTINCT w.scheme)                       AS schemes;
```

```cypher
// q007_flagged_works_in_panchayat.cypher
// INTENT: flagged_works
// SLOTS:  $gp_code (INT64), $fy_start (DATE), $fy_end (DATE)
// ANSWERS: "Which works have questions against them?"
MATCH (p:Panchayat {gp_code: $gp_code})<-[:LOCATED_IN]-(w:Work)
WHERE w.sanction_date >= $fy_start AND w.sanction_date <= $fy_end
OPTIONAL MATCH (ph:Photo)-[:EVIDENCES]->(w)
OPTIONAL MATCH (ph)-[d:DUPLICATE_OF]->(:Photo)
OPTIONAL MATCH (s:SatelliteObservation)-[:IMAGES]->(w)
OPTIONAL MATCH (c:Contract)-[:FUNDS]->(w)-[:LOCATED_IN]->(p)
OPTIONAL MATCH (c)-[:AWARDED_TO]->(v:Vendor)
WITH w,
     count(DISTINCT d)                                   AS dup_photos,
     max(CASE WHEN s.change_detected = false
              AND w.satellite_verifiable THEN 1 ELSE 0 END) AS sat_nochange,
     v.canonical_name                                    AS vendor
WHERE dup_photos > 0 OR sat_nochange = 1
RETURN w.work_id, w.work_name, w.sanctioned_amount,
       w.claimed_completion_date, dup_photos, sat_nochange, vendor
ORDER BY w.sanctioned_amount DESC
LIMIT 10;
```

```python
# src/saakshi/kosh/queries/__init__.py
"""
⭐ THE R2 ENFORCEMENT POINT.

Only queries registered here can execute. The intent router returns an
intent name; this maps it to a vetted, unit-tested .cypher file. There is
no code path anywhere in SAAKSHI that executes generated Cypher.
"""
from pathlib import Path
import kuzu

_DIR = Path(__file__).parent
_REGISTRY: dict[str, Path] = {
    "panchayat_year_summary": _DIR / "q001_panchayat_year_summary.cypher",
    "work_detail":            _DIR / "q002_work_detail.cypher",
    "flagged_works":          _DIR / "q007_flagged_works_in_panchayat.cypher",
    "wage_delay":             _DIR / "q012_wage_delay_for_panchayat.cypher",
    "vendor_concentration":   _DIR / "q018_vendor_concentration_block.cypher",
    "single_bid_rate":        _DIR / "q019_single_bid_rate.cypher",
    "recovery_ledger":        _DIR / "q031_recovery_by_district.cypher",
    # ... ~40 total
}


class UnknownIntent(Exception): ...


def run(conn: kuzu.Connection, intent: str, params: dict):
    if intent not in _REGISTRY:
        raise UnknownIntent(
            f"'{intent}' is not a registered query. "
            "SAAKSHI does not generate queries. See PLAN.md R2."
        )
    return conn.execute(_REGISTRY[intent].read_text(encoding="utf-8"), params)
```

> **Show this file to a technical judge.** It is a fifteen-line, verifiable proof that your system cannot hallucinate a database query. That is worth more than any accuracy number you could quote.

---

## 6. Phase 3 — CHITRAGUPTA: the four detectors

### 6.1 ① Photo forensics — build this first

**Highest value per line of code in the entire project.** This is the CAG "identical photographs across construction stages" fraud, automated.

```python
# src/saakshi/chitragupta/photos.py
"""
Detector ①: Photo forensics.

CAG (Karnataka MGNREGA, 2026) found that identical photographs were
uploaded across different construction stages to fake progress. They
found it by looking. We find it with a perceptual hash.

Four checks:
  (a) pHash/dHash near-duplicate across the ENTIRE corpus
  (b) EXIF GPS vs the work's declared location
  (c) EXIF timestamp vs muster-roll / claimed-stage date
  (d) device clustering — one phone at N sites in one hour
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta
import imagehash, exifread
from PIL import Image
from math import radians, sin, cos, asin, sqrt

PHASH_SIZE = 8              # 64-bit hash
DUP_THRESHOLD = 5           # Hamming ≤ 5 ⇒ near-identical
GEO_TOLERANCE_KM = 2.0      # a completion photo should be AT the work


@dataclass(slots=True)
class PhotoRecord:
    photo_id: str
    path: Path
    phash: str
    dhash: str
    lat: float | None
    lon: float | None
    taken_at: datetime | None
    device: str | None


# ---------- (a) near-duplicate detection ----------
def compute_hashes(path: Path) -> tuple[str, str]:
    with Image.open(path) as im:
        im = im.convert("RGB")
        return (str(imagehash.phash(im, hash_size=PHASH_SIZE)),
                str(imagehash.dhash(im, hash_size=PHASH_SIZE)))


def find_duplicates(records: list[PhotoRecord],
                    threshold: int = DUP_THRESHOLD
                    ) -> list[tuple[str, str, int]]:
    """
    BK-tree over pHash. O(n log n)-ish instead of O(n²).
    For a hackathon-scale corpus (<1M) a bucketed prefix scan is
    plenty; for national scale, swap in FAISS Hamming.
    """
    import pybktree
    def dist(a, b):
        return imagehash.hex_to_hash(a[1]) - imagehash.hex_to_hash(b[1])

    tree = pybktree.BKTree(dist, [(r.photo_id, r.phash) for r in records])
    out, seen = [], set()
    for r in records:
        for d, (pid, _) in tree.find((r.photo_id, r.phash), threshold):
            if pid == r.photo_id:
                continue
            key = tuple(sorted((r.photo_id, pid)))
            if key in seen:
                continue
            seen.add(key)
            out.append((key[0], key[1], d))
    return out


# ---------- (b) geo mismatch ----------
def haversine_km(lat1, lon1, lat2, lon2) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
    a = (sin((lat2 - lat1) / 2) ** 2
         + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371.0 * asin(sqrt(a))


def geo_mismatch(photo: PhotoRecord, work_lat: float, work_lon: float
                 ) -> tuple[bool, float | None]:
    if photo.lat is None or photo.lon is None:
        return False, None            # missing EXIF is not evidence of fraud
    d = haversine_km(photo.lat, photo.lon, work_lat, work_lon)
    return d > GEO_TOLERANCE_KM, d


# ---------- (d) impossible device itinerary ----------
def impossible_itinerary(records: list[PhotoRecord],
                         window_minutes: int = 60,
                         max_sites: int = 3) -> list[dict]:
    """
    One device geo-tagging attendance at many distinct sites inside one
    hour. Physically impossible; administratively common.
    """
    by_device: dict[str, list[PhotoRecord]] = {}
    for r in records:
        if r.device and r.taken_at and r.lat is not None:
            by_device.setdefault(r.device, []).append(r)

    flags = []
    for device, rs in by_device.items():
        rs.sort(key=lambda x: x.taken_at)
        for i, anchor in enumerate(rs):
            window = [x for x in rs[i:]
                      if x.taken_at - anchor.taken_at
                      <= timedelta(minutes=window_minutes)]
            sites = {(round(x.lat, 3), round(x.lon, 3)) for x in window}
            if len(sites) > max_sites:
                span = max(haversine_km(*a, *b)
                           for a in sites for b in sites if a != b)
                flags.append({
                    "device": device,
                    "start": anchor.taken_at,
                    "distinct_sites": len(sites),
                    "max_span_km": round(span, 1),
                    "photo_ids": [x.photo_id for x in window],
                })
    return flags
```

**Expected output:**

```
── CHITRAGUPTA ① PHOTO FORENSICS ───────────────────────────────
corpus: 412,883 photos · elapsed 00:07:41

(a) NEAR-DUPLICATES ................................ 1,284 pairs
    of which cross-WORK ............................   311 pairs
    of which cross-DISTRICT ........................    47 pairs  ⚠
    tightest match: hamming 0/64

    ⚠ nmms_88213.jpg  ←→  nmms_71104.jpg   hamming 0
       work KA-KLB-2026-00412 "Farm pond, survey 112/3"
       work KA-KOP-2026-00189 "Farm pond, survey 44/1"
       distance between works: 61.3 km
       claimed stages: "completion" / "completion"

(b) GEO MISMATCH (> 2.0 km) ........................   892 photos
(c) TIMESTAMP OUTSIDE SANCTION WINDOW ..............   203 photos
(d) IMPOSSIBLE DEVICE ITINERARY ....................    18 devices
    ⚠ device "Redmi 9A"  8 distinct sites in 47 min, span 34.2 km
────────────────────────────────────────────────────────────────
```

> **That block is your demo's opening beat.** Seven minutes of compute reproducing a class of finding that took CAG a manual audit — and extending it from a 39-panchayat sample to the whole corpus.

### 6.2 ② Payment structure

```python
# src/saakshi/chitragupta/payments.py
"""
Detector ②: Payment structure. Fully unsupervised — no labels needed.

(a) threshold splitting   ← the CAG Koppal check-dam fraud
(b) Benford's law
(c) Payment Heterogeneity Index (arXiv:2605.12547)
(d) temporal impossibility ← the CAG "462 instances" fraud
"""
import numpy as np, polars as pl
from scipy import stats

# Statutory tender thresholds (₹). CONFIGURE PER STATE — these vary,
# and getting them wrong produces false positives.
THRESHOLDS = [100_000, 250_000, 500_000, 1_000_000, 2_500_000]


def threshold_splitting(df: pl.DataFrame,
                        window_frac: float = 0.10) -> pl.DataFrame:
    """
    Works whose value sits suspiciously just BELOW a tender threshold,
    especially when the same vendor/panchayat has several such works
    close together in time.

    CAG, Koppal (Yelburga taluk): "a check dam split into two smaller
    works to bypass tendering."
    """
    out = []
    for t in THRESHOLDS:
        lo, hi = t * (1 - window_frac), t
        band = df.filter(
            (pl.col("sanctioned_amount") >= lo) &
            (pl.col("sanctioned_amount") < hi)
        )
        if band.is_empty():
            continue
        # Sibling works: same GP + same vendor + within 60 days
        sib = (band
               .group_by(["gp_code", "vendor_id"])
               .agg(pl.len().alias("n_works"),
                    pl.col("sanctioned_amount").sum().alias("combined"),
                    pl.col("work_id").alias("work_ids"))
               .filter((pl.col("n_works") >= 2) &
                       (pl.col("combined") >= t))   # ← together they'd have
               .with_columns(pl.lit(t).alias("threshold_evaded")))
        out.append(sib)
    return pl.concat(out) if out else pl.DataFrame()


def benford_first_digit(amounts: np.ndarray) -> dict:
    """Chi-square against Benford. Use as a WEAK signal only."""
    amounts = amounts[amounts > 0]
    first = np.array([int(str(int(a))[0]) for a in amounts])
    observed = np.array([(first == d).sum() for d in range(1, 10)])
    expected = np.array([np.log10(1 + 1 / d) for d in range(1, 10)]) * len(first)
    chi2, p = stats.chisquare(observed, expected)
    return {"chi2": float(chi2), "p_value": float(p),
            "n": int(len(first)), "deviates": bool(p < 0.01)}


def temporal_impossibility(payments: pl.DataFrame,
                           works: pl.DataFrame) -> pl.DataFrame:
    """
    ⭐ The CAG "462 instances" check.

    "462 instances of payments made for foundation/lintel/roofing stages
     on houses already completed earlier."

    This is one date comparison. It does not run anywhere in India.
    """
    j = payments.join(works, on="work_id", how="inner")
    return (j
        .filter(
            (pl.col("payment_date") > pl.col("claimed_completion_date"))
            & pl.col("stage").is_in(["foundation", "lintel", "roofing", "plinth"])
        )
        .select(["work_id", "payment_id", "stage",
                 "payment_date", "claimed_completion_date", "amount"])
        .with_columns(
            (pl.col("payment_date") - pl.col("claimed_completion_date"))
            .dt.total_days().alias("days_after_completion"),
            pl.lit("STAGE_PAYMENT_AFTER_COMPLETION").alias("flag"),
        ))
```

**Expected output:**

```
── CHITRAGUPTA ② PAYMENT STRUCTURE ─────────────────────────────
(a) THRESHOLD SPLITTING
    threshold ₹5,00,000 → 34 sibling groups
    ⚠ Yelburga block, vendor V-04412: 2 works, ₹2.4L + ₹2.9L
      = ₹5.3L combined, both dated within 11 days
      → would have crossed the ₹5L tender threshold as one work

(b) BENFORD (bill amounts, n=48,221)
    chi2 = 412.8   p < 0.001   ⚠ deviates
    excess of leading digit 4 (+18% vs expected)

(c) PAYMENT HETEROGENEITY INDEX
    vendors screened 2,914 · structurally distinct 19 (0.65%)
    (cf. published 0.6% on UK municipal data — in family)

(d) TEMPORAL IMPOSSIBILITY
    ⚠ 462 stage payments AFTER claimed completion date
      median lag: 41 days · total value ₹1.19 crore
      ↳ matches CAG Karnataka finding exactly.  ✓ VALIDATED
────────────────────────────────────────────────────────────────
```

> **The line `↳ matches CAG Karnataka finding exactly. ✓ VALIDATED` is the most valuable line in this entire project.** It converts "we built a thing" into "we independently rediscovered a published CAG finding from public data, automatically."

### 6.3 ③ Network / collusion

```python
# src/saakshi/chitragupta/network.py
"""
Detector ③: Network collusion.

Computes the standard World Bank / DIGIWHIST red flags that
NO INDIAN BODY PUBLISHES:
  · single-bid rate
  · repeat-winner concentration (HHI)
  · award-vs-estimate variance
  · advertisement-period shortening
  · network core membership, supplier eigenvector centrality

R3: LightGBM baseline FIRST. GADBench (arXiv:2306.12251) found tree
    ensembles beat task-specific GNNs. A GAT must BEAT this to ship.
"""
import networkx as nx, polars as pl, numpy as np


def red_flags_by_entity(awards: pl.DataFrame) -> pl.DataFrame:
    """⭐ India's first single-bid rate table."""
    return (awards
        .group_by("org_chain")
        .agg(
            pl.len().alias("n_tenders"),
            (pl.col("num_bidders") == 1).sum().alias("n_single_bid"),
            pl.col("award_value").sum().alias("total_awarded"),
            ((pl.col("award_value") - pl.col("estimate_value"))
             / pl.col("estimate_value")).mean().alias("mean_award_premium"),
            pl.col("winner_name").n_unique().alias("n_distinct_winners"),
        )
        .with_columns(
            (pl.col("n_single_bid") / pl.col("n_tenders"))
                .alias("single_bid_rate"),           # ← THE indicator
            (pl.col("n_distinct_winners") / pl.col("n_tenders"))
                .alias("winner_diversity"),
        )
        .sort("single_bid_rate", descending=True))


def cobid_graph(bids: pl.DataFrame) -> nx.Graph:
    """Vendors are adjacent if they bid on the same tender."""
    G = nx.Graph()
    for (tid,), grp in bids.group_by(["tender_id"]):
        vendors = grp["vendor_id"].to_list()
        for i, a in enumerate(vendors):
            for b in vendors[i + 1:]:
                if G.has_edge(a, b):
                    G[a][b]["weight"] += 1
                else:
                    G.add_edge(a, b, weight=1)
    return G


def network_features(G: nx.Graph) -> pl.DataFrame:
    """
    SHAP analysis in arXiv:2512.19491 found NETWORK-derived features
    (core membership, eigenvector centrality) DOMINATE classic red flags.
    """
    core = nx.core_number(G)
    eig  = nx.eigenvector_centrality_numpy(G) if G.number_of_edges() else {}
    btw  = nx.betweenness_centrality(G, k=min(500, G.number_of_nodes()))
    clu  = nx.clustering(G, weight="weight")
    return pl.DataFrame({
        "vendor_id": list(G.nodes()),
        "core_number":    [core.get(v, 0)  for v in G.nodes()],
        "eigenvector":    [eig.get(v, 0.0) for v in G.nodes()],
        "betweenness":    [btw.get(v, 0.0) for v in G.nodes()],
        "clustering":     [clu.get(v, 0.0) for v in G.nodes()],
        "degree":         [G.degree(v)     for v in G.nodes()],
    })


def train_pu(features: pl.DataFrame,
             positives: set[str],
             n_estimators: int = 400):
    """
    Positive-Unlabeled learning (Elkan-Noto), per arXiv:2512.19491.

    There are no confirmed NEGATIVES in procurement. Never pretend
    there are. Positives seed from:
      · CAG published findings
      · CVC / CCI sanction records
      · ⭐ VERIFIED CITIZEN REPORTS   ← the novel label source (N2)
    """
    import lightgbm as lgb
    from sklearn.model_selection import StratifiedKFold

    X = features.drop("vendor_id").to_numpy()
    s = np.array([1 if v in positives else 0
                  for v in features["vendor_id"]])   # labelled-positive flag

    # Step 1: non-traditional classifier P(s=1|x)
    clf = lgb.LGBMClassifier(n_estimators=n_estimators, is_unbalance=True)
    oof = np.zeros(len(s))
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=42).split(X, s):
        clf.fit(X[tr], s[tr])
        oof[te] = clf.predict_proba(X[te])[:, 1]

    # Step 2: c = P(s=1|y=1), estimated on the labelled positives
    c = float(oof[s == 1].mean())
    # Step 3: calibrate P(y=1|x) = P(s=1|x) / c
    p_y = np.clip(oof / max(c, 1e-6), 0.0, 1.0)

    clf.fit(X, s)   # final fit on everything
    return clf, c, p_y
```

**Expected output — India's first single-bid rate table:**

```
── CHITRAGUPTA ③ NETWORK  ·  PROCUREMENT RED FLAGS ─────────────
⭐ No Indian body publishes these. This is the first computation.

top procuring entities by single-bid rate (n_tenders ≥ 20)

org_chain                          n    single-bid   award    winner
                                        rate         premium  diversity
───────────────────────────────────────────────────────────────────────
RDPR::Koppal::Yelburga            16      68.8%      +2.1%      0.19  ⚠
RDPR::Kalaburagi::Kamalapur       23      52.2%      +1.4%      0.30  ⚠
PWD::Ballari::Sandur              41      31.7%      -3.2%      0.54
...
───────────────────────────────────────────────────────────────────────
NATIONAL (all entities, n=97,884)        ~XX.X%      ← FIRST EVER

co-bidding graph: 2,914 vendors · 11,208 edges · 41 communities
PU model: c = 0.31 · AUC-PU 0.79 · top-decile lift 3.4×
```

### 6.4 ④ Satellite — and the honesty gate

```python
# src/saakshi/chitragupta/satellite.py
"""
Detector ④: Bi-temporal change detection on FREE Sentinel-2.

⚠⚠ THE HONESTY GATE ⚠⚠
At 10 m GSD one pixel is 100 m². A rural toilet (~1.5×1.5 m) and a hand
pump are PHYSICALLY INVISIBLE. Prithvi-EO-2.0 across 19 OOD events:
IoU 52% cropland, IoU ≈ 4% BUILT-UP (arXiv:2606.07780). All GFMs lose
15-20% OOD (arXiv:2605.29330).

⇒ We refuse to analyse asset types we cannot see, and we say so in the
  output. A "no change" result is a TRIGGER FOR HUMAN VERIFICATION,
  never a verdict.

Data: Element84 Earth Search STAC, Sentinel-2 L2A COGs. Free. No auth.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
import numpy as np, rasterio
from rasterio.windows import from_bounds
from pystac_client import Client

STAC_URL = "https://earth-search.aws.element84.com/v1"

# ⭐ THE HONESTY GATE. Everything else in this file is downstream of it.
SATELLITE_VERIFIABLE = {
    "farm_pond":        True,   # NDWI water signature
    "check_dam":        True,
    "percolation_tank": True,
    "road":             True,   # linear, tens of m over km
    "canal":            True,
    "land_levelling":   True,   # NDVI / bare-soil change
    "bunding":          True,
    "housing_cluster":  True,   # ≥ 5 units
    # ---- below detection limit at 10 m ----
    "toilet":           False,
    "hand_pump":        False,
    "soak_pit":         False,
    "single_house":     False,
    "compost_pit":      False,
    "cattle_shed":      False,
}

BAND = {"green": "green", "red": "red", "nir": "nir", "swir16": "swir16"}


@dataclass
class ChangeResult:
    work_id: str
    verifiable: bool
    reason: str
    ndwi_delta: float | None = None
    ndvi_delta: float | None = None
    ndbi_delta: float | None = None
    change_detected: bool | None = None
    confidence: str = "N/A"          # HIGH | LOW | N/A
    scene_before: str | None = None
    scene_after: str | None = None


def _search(lat, lon, target: date, window_days=30, max_cloud=20):
    cat = Client.open(STAC_URL)
    items = list(cat.search(
        collections=["sentinel-2-l2a"],
        intersects={"type": "Point", "coordinates": [lon, lat]},
        datetime=f"{target - timedelta(days=window_days)}/"
                 f"{target + timedelta(days=window_days)}",
        query={"eo:cloud_cover": {"lt": max_cloud}},
        max_items=10,
    ).items())
    if not items:
        return None
    return min(items, key=lambda i: abs(
        (i.datetime.date() - target).days))


def _patch(item, lat, lon, band: str, half_m: int = 150) -> np.ndarray:
    """~300×300 m window around the work. Reflectance, scaled."""
    href = item.assets[BAND[band]].href
    d = half_m / 111_320
    with rasterio.open(href) as src:
        from rasterio.warp import transform_bounds
        b = transform_bounds("EPSG:4326", src.crs,
                             lon - d, lat - d, lon + d, lat + d)
        arr = src.read(1, window=from_bounds(*b, src.transform)).astype("float32")
    return arr / 10_000.0


def _index(a, b):
    """Generic normalized difference, guarded against /0."""
    return np.divide(a - b, a + b, out=np.zeros_like(a), where=(a + b) != 0)


def verify_work(work_id: str, asset_type: str, lat: float, lon: float,
                sanction_date: date, completion_date: date) -> ChangeResult:
    # ---- the honesty gate ----
    if not SATELLITE_VERIFIABLE.get(asset_type, False):
        return ChangeResult(
            work_id=work_id, verifiable=False,
            reason=(f"Asset type '{asset_type}' is below the 10 m Sentinel-2 "
                    f"detection limit (1 px = 100 m²). SAAKSHI does not "
                    f"analyse it. Route to citizen verification."),
        )

    before = _search(lat, lon, sanction_date - timedelta(days=15))
    after  = _search(lat, lon, completion_date + timedelta(days=15))
    if before is None or after is None:
        return ChangeResult(work_id=work_id, verifiable=True,
                            reason="No cloud-free scene in window.",
                            confidence="N/A")

    g0, n0, r0, s0 = (_patch(before, lat, lon, b)
                      for b in ("green", "nir", "red", "swir16"))
    g1, n1, r1, s1 = (_patch(after,  lat, lon, b)
                      for b in ("green", "nir", "red", "swir16"))

    ndwi_d = float(np.nanmean(_index(g1, n1)) - np.nanmean(_index(g0, n0)))
    ndvi_d = float(np.nanmean(_index(n1, r1)) - np.nanmean(_index(n0, r0)))
    ndbi_d = float(np.nanmean(_index(s1, n1)) - np.nanmean(_index(s0, n0)))

    if asset_type in ("farm_pond", "check_dam", "percolation_tank"):
        detected, conf = ndwi_d > 0.10, "HIGH" if abs(ndwi_d) > 0.10 else "LOW"
    elif asset_type in ("road", "canal", "land_levelling", "bunding"):
        detected, conf = ndbi_d > 0.05, "LOW"      # always LOW — see below
    else:
        detected, conf = ndbi_d > 0.08, "LOW"

    return ChangeResult(
        work_id=work_id, verifiable=True,
        reason="Bi-temporal Sentinel-2 L2A, 10 m GSD.",
        ndwi_delta=ndwi_d, ndvi_delta=ndvi_d, ndbi_delta=ndbi_d,
        change_detected=detected, confidence=conf,
        scene_before=before.id, scene_after=after.id,
    )
```

**Expected output:**

```
── CHITRAGUPTA ④ SATELLITE ─────────────────────────────────────
works submitted ............................ 14,203
  ⛔ SKIPPED — below detection limit ........  9,118  (64.2%)
       toilet 6,402 · hand_pump 1,880 · soak_pit 836
       → routed to PRAMAAN citizen verification
  ⚠  no cloud-free scene ...................    412
  ✓  analysed ..............................  4,673

of the 4,673 analysed:
  change detected ..........................  4,204  (90.0%)
  NO CHANGE DETECTED .......................    469  (10.0%)  ⚠

  ⚠ KA-KLB-2026-00412  farm_pond  ₹4,20,000
     before S2A_MSIL2A_20260308  after S2A_MSIL2A_20260619
     NDWI Δ = +0.012   (threshold +0.10)
     → NO detectable surface-water feature appeared
     confidence: LOW
     ⚠ NOT DISPOSITIVE. 10 m GSD. Small ponds may fall below the
       detection limit. This is a TRIGGER for human verification.
────────────────────────────────────────────────────────────────
```

> **Note that 64.2% skip rate.** Most judges will expect you to hide it. **Lead with it.** "We refuse to analyse two-thirds of works because we physically cannot see them, and here is the pixel arithmetic" is the single most credible thing you can say in a technical Q&A.

### 6.5 Evidence assembly — explicitly NOT a score

```python
# src/saakshi/chitragupta/fuse.py
"""
⚠ THIS MODULE DOES NOT PRODUCE A SCORE.

arXiv:2309.01462 (IRT validation of 15 red flags on Italy's national
contracts DB): red flags are MULTIDIMENSIONAL AND NON-SUPERIMPOSABLE.
A single composite corruption-risk index is STATISTICALLY UNJUSTIFIED.

So we assemble an EVIDENCE BUNDLE: four independent signals, each with
its own confidence and its own stated failure mode. A human weighs them.
"""
from pydantic import BaseModel
from typing import Literal

Confidence = Literal["HIGH", "MEDIUM", "LOW", "N/A"]


class Signal(BaseModel):
    detector: Literal["photo", "payment", "network", "satellite", "citizen"]
    fired: bool
    confidence: Confidence
    finding: str                 # one plain sentence a citizen can read
    method: str                  # reproducible description
    limitation: str              # ⭐ R5 — mandatory, never empty
    evidence_refs: list[str]


class EvidenceBundle(BaseModel):
    work_id: str
    signals: list[Signal]
    unknowns: list[str]          # ⭐ "What we do not know" — mandatory

    @property
    def fired_count(self) -> int:
        return sum(s.fired for s in self.signals)

    @property
    def opens_case(self) -> bool:
        """
        A case needs BOTH:
          · ≥ 2 independent machine signals, AND
          · ≥ 1 HIGH-confidence signal
        A single LOW-confidence satellite result NEVER opens a case.
        """
        fired = [s for s in self.signals if s.fired]
        return len(fired) >= 2 and any(s.confidence == "HIGH" for s in fired)
```

---

## 7. Phase 4 — NAAM-MILAN: Indic entity resolution

```python
# src/saakshi/naammilan/canonicalize.py
"""
Indic name canonicalization.

Two records may denote one person across scripts, spellings and
transliterations. This is Novelty Gap N4: there is NO published
Indian-name entity resolution benchmark.

  रामेश्वर सिद्दप्पा  ·  Rameshwar Siddappa
  ರಾಮೇಶ್ವರ ಸಿದ್ದಪ್ಪ    ·  R. Siddappa

Aksharantar / IndicXlit: 26M pairs, 21 languages, 12 scripts
(arXiv:2205.03018). Character-level OT alignment for variant
spellings (arXiv:1907.10165).

⚠ PRIVACY: we hash. Raw Aadhaar is NEVER ingested, stored or matched.
"""
import hashlib, unicodedata, re
from ai4bharat.transliteration import XlitEngine

_XLIT = XlitEngine(beam_width=4, rescore=True)   # Indic → Roman

# Indic-aware phonetic folds. Devanagari/Kannada/Telugu speakers
# routinely swap these in Roman transliteration.
_FOLDS = [
    (r"aa", "a"), (r"ee", "i"), (r"oo", "u"),
    (r"sh", "s"), (r"ss", "s"), (r"th", "t"), (r"dh", "d"),
    (r"bh", "b"), (r"gh", "g"), (r"kh", "k"), (r"ph", "f"),
    (r"ck", "k"), (r"w",  "v"), (r"y$", "i"),
    (r"(.)\1+", r"\1"),          # collapse doubles
]


def to_roman(name: str) -> str:
    if any(ord(c) > 0x0900 for c in name):
        try:
            return _XLIT.translit_sentence(name, lang_code="hi")
        except Exception:
            pass
    return name


def phonetic_key(name: str) -> str:
    """Aggressive fold. Blocking key — NOT the match decision."""
    s = unicodedata.normalize("NFKD", to_roman(name)).lower()
    s = re.sub(r"[^a-z\s]", "", s)
    for pat, rep in _FOLDS:
        s = re.sub(pat, rep, s)
    tokens = sorted(t for t in s.split() if len(t) > 1)   # order-invariant
    return "".join(tokens)


def name_hash(name: str, salt: bytes) -> str:
    """Salted hash. The raw name never leaves the ingest boundary."""
    return hashlib.blake2b(
        phonetic_key(name).encode(), key=salt, digest_size=16).hexdigest()
```

```python
# src/saakshi/naammilan/resolve.py
"""
Calibrated ER with splink (Fellegi-Sunter + EM).

⭐ THE DESIGN DECISION THAT MATTERS MOST IN THIS FILE:
   SAAKSHI NEVER ASSERTS "THIS IS A GHOST BENEFICIARY."
   It emits a POSTERIOR. A human decides.

Why: the Aadhaar-seeding literature (Drèze/Khera/Somanchi;
Muralidharan/Niehaus/Sukhtankar across 15 MILLION beneficiaries) shows
every anti-fraud intervention in Indian welfare has produced EXCLUSION
ERRORS. A hard classifier on a beneficiary register deletes real poor
people at scale. A calibrated posterior cannot.
"""
from splink import Linker, SettingsCreator, DuckDBAPI
import splink.comparison_library as cl

SETTINGS = SettingsCreator(
    link_type="dedupe_only",
    blocking_rules_to_generate_predictions=[
        "l.phonetic_key = r.phonetic_key",
        "l.gp_code = r.gp_code AND substr(l.phonetic_key,1,4) "
        "= substr(r.phonetic_key,1,4)",
    ],
    comparisons=[
        cl.JaroWinklerAtThresholds("name_roman", [0.9, 0.8, 0.7]),
        cl.ExactMatch("gp_code"),
        cl.LevenshteinAtThresholds("father_name_roman", [1, 3]),
        cl.AbsoluteDateDifferenceAtThresholds(
            "dob", input_is_string=True,
            metrics=["year"], thresholds=[1, 5]),
    ],
    retain_intermediate_calculation_columns=True,
)


def resolve(df, threshold: float = 0.80):
    linker = Linker(df, SETTINGS, DuckDBAPI())
    linker.training.estimate_probability_two_random_records_match(
        ["l.name_roman = r.name_roman AND l.gp_code = r.gp_code"],
        recall=0.7)
    linker.training.estimate_u_using_random_sampling(max_pairs=5_000_000)
    linker.training.estimate_parameters_using_expectation_maximisation(
        "l.phonetic_key = r.phonetic_key")

    preds = linker.inference.predict(threshold_match_probability=threshold)
    return preds.as_pandas_dataframe()
```

**Expected output:**

```
── NAAM-MILAN ──────────────────────────────────────────────────
records          412,883 across 5 registers
blocking pairs     8.2M  (from 8.5e10 naive — 10,000× reduction)
above threshold   11,204 clusters

⚠ cluster NM-KLB-88213   posterior 0.83
  RAMESHWAR SIDDAPPA        NREGASoft   gp 226534  card KN-03-004-001/1129
  Rameshwar Siddappa        PMAY-G      gp 226534
  ರಾಮೇಶ್ವರ ಸಿದ್ದಪ್ಪ           State PDS   gp 226534
  R. Siddappa               PM-KISAN    gp 226534

  ⚠ THIS IS NOT EVIDENCE OF FRAUD.
    One person may legitimately be enrolled in four schemes.
    It becomes a signal ONLY when combined with a payment anomaly
    or a citizen report. Human adjudication required.
────────────────────────────────────────────────────────────────
```

---

## 8. Phase 5 — VAANI: the voice layer

### 8.1 ⭐ The intent router — the R2 enforcement point

```python
# src/saakshi/vaani/intent.py
"""
⭐ THE MOST IMPORTANT FILE IN THE REPOSITORY.

The LLM classifies an intent from a CLOSED SET and extracts slots.
It NEVER writes a query. It NEVER sees the database.

WHY (all measured, not assumed):
  · 54-69% NL→query execution accuracy for strong COMMERCIAL models on
    provenance-aware graphs; 6-19% for 7B open models, WHICH NEVER
    ABSTAIN on unanswerable questions          (arXiv:2607.25243)
  · best correctness verifier: 0.82 AUROC, at an operating point that
    ANSWERS ONLY 27% OF QUESTIONS at 24% selective risk (arXiv:2607.06799)
  · fine-tuned verifiers fall 0.79 → 0.66 on unseen schemas; scaling,
    distillation and cross-benchmark training ALL FAIL to close it
  · schema linking DOESN'T HELP — a linker with 96.5% gold-table recall
    is statistically indistinguishable from none  (arXiv:2606.29733)

⇒ ~40 vetted parameterised queries turn a 60% problem into a >95% one,
  AND make every answer reproducible — which matters because a case
  file may end up in a legal proceeding, and financial ML pipelines
  are not even deterministic across re-runs (arXiv:2605.23955).
"""
from enum import StrEnum
from pydantic import BaseModel, Field


class Intent(StrEnum):
    PANCHAYAT_YEAR_SUMMARY = "panchayat_year_summary"
    FLAGGED_WORKS          = "flagged_works"
    WORK_DETAIL            = "work_detail"
    WAGE_DELAY             = "wage_delay"
    MY_PAYMENTS            = "my_payments"
    VENDOR_CONCENTRATION   = "vendor_concentration"
    SINGLE_BID_RATE        = "single_bid_rate"
    RECOVERY_LEDGER        = "recovery_ledger"
    CASE_STATUS            = "case_status"
    FILE_REPORT            = "file_report"
    # ... ~40 total
    UNKNOWN                = "unknown"          # ⭐ MUST exist


class Slots(BaseModel):
    gp_name:      str | None = None
    district:     str | None = None
    gp_code:      int | None = None
    scheme:       str | None = None
    fiscal_year:  str | None = None
    work_id:      str | None = None
    case_id:      str | None = None


class Classification(BaseModel):
    intent:     Intent
    slots:      Slots
    confidence: float = Field(ge=0.0, le=1.0)
    needs_confirmation: bool = True     # ⭐ default TRUE, always


SYSTEM_PROMPT = """\
You classify a citizen's spoken question into EXACTLY ONE intent from
the provided list, and extract slots.

RULES:
1. You do NOT answer the question. You do NOT write queries or SQL.
2. If the question does not clearly match an intent, return "unknown".
   Returning "unknown" is CORRECT and PREFERRED over guessing.
3. Extract only slots explicitly present. Never infer a village name.
4. The input is ASR output with 16-35% word error rate. Village names
   are frequently mis-transcribed. If a village name is uncertain,
   still extract it — the caller will confirm it verbally.
5. Output only the JSON schema. No prose.
"""
```

### 8.2 ASR with the failure modes designed in

```python
# src/saakshi/vaani/asr.py
"""
ASR with the three known Indic failure modes handled explicitly.

MEASURED REALITY (arXiv:2602.03868, 10,934 REAL field recordings):
  Hindi  best-case WER 16.2%
  Odia   best-case WER 35.1%  ← and ONLY with speaker diarization
  diarization + best-speaker selection cuts WER by UP TO 66% on
  multi-speaker audio — and a village phone call is ALWAYS multi-speaker

  WER RISES with inter-district distance from training data (2606.09345)

  21 of 100 model-language pairs SILENTLY EMIT THE WRONG SCRIPT —
  fluent, plausible, and INVISIBLE TO WER (arXiv:2604.08786).
  Script-aware prompting: mean SFR 71.2% → 97.7%; Urdu 6.5% → 97.0%

⇒ DESIGN: no free-form dictation. Slot-filling + verbal confirmation
  + DTMF on EVERY prompt + script guard + diarization.
"""
import unicodedata, httpx

SCRIPT_RANGES = {
    "hi": (0x0900, 0x097F),   # Devanagari
    "kn": (0x0C80, 0x0CFF),   # Kannada
    "te": (0x0C00, 0x0C7F),   # Telugu
    "ta": (0x0B80, 0x0BFF),   # Tamil
    "bn": (0x0980, 0x09FF),   # Bengali
    "or": (0x0B00, 0x0B7F),   # Odia
    "gu": (0x0A80, 0x0AFF),
    "ml": (0x0D00, 0x0D7F),
    "pa": (0x0A00, 0x0A7F),
    "mr": (0x0900, 0x097F),
}


def script_fidelity_rate(text: str, lang: str) -> float:
    """
    Reference-free SFR (arXiv:2604.08786). Catches the failure that
    WER cannot see: fluent output in the WRONG script.
    """
    lo, hi = SCRIPT_RANGES.get(lang, (0, 0x10FFFF))
    letters = [c for c in text if unicodedata.category(c).startswith("L")]
    if not letters:
        return 0.0
    return sum(lo <= ord(c) <= hi for c in letters) / len(letters)


async def transcribe(audio: bytes, lang: str, cfg) -> dict:
    """Bhashini ASR + diarization + script guard."""
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(
            "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
            headers={"Authorization": cfg.bhashini_key},
            json={
                "pipelineTasks": [{
                    "taskType": "asr",
                    "config": {
                        "language": {"sourceLanguage": lang},
                        "audioFormat": "wav",
                        "samplingRate": 8000,          # telephony
                        "preProcessors": ["vad", "denoiser"],
                        # ⭐ up to 66% WER reduction on multi-speaker audio
                        "postProcessors": ["diarization"],
                    },
                }],
                "inputData": {"audio": [{"audioContent": audio.hex()}]},
            })
        out = r.json()

    text = out["pipelineResponse"][0]["output"][0]["source"]
    sfr = script_fidelity_rate(text, lang)

    if sfr < 0.60:                       # ⭐ script collapse detected
        return {"text": "", "sfr": sfr,
                "action": "RETRY_WITH_SCRIPT_PROMPT"}

    return {"text": text, "sfr": sfr, "action": "OK"}
```

### 8.3 The IVR state machine

```python
# src/saakshi/vaani/ivr.py
"""
IVR state machine.

DESIGN RULES, each traceable to a measured constraint:
  1. DTMF fallback on EVERY prompt.  85.5% of households have a phone;
     only 48.4% of rural women 15+ own one. It may not be her phone.
  2. Verbal confirmation before ANY action. Hindi WER 16.2%.
  3. Max 3 slots per call. Every extra slot multiplies the error rate.
  4. Answers are TEMPLATED, then translated. Never LLM-generated prose.
  5. Explicit uncertainty spoken aloud: "Saakshi can be wrong."
"""
from enum import StrEnum
from fastapi import APIRouter, Form
from fastapi.responses import Response

router = APIRouter(prefix="/ivr")


class State(StrEnum):
    GREETING          = "greeting"
    LANGUAGE_SELECT   = "language_select"
    MAIN_MENU         = "main_menu"
    ASK_VILLAGE       = "ask_village"
    CONFIRM_VILLAGE   = "confirm_village"     # ⭐ never skippable
    SPEAK_SUMMARY     = "speak_summary"
    SPEAK_FLAGS       = "speak_flags"
    ASK_VERIFICATION  = "ask_verification"    # ⭐ the label moment
    THANK_AND_CASE    = "thank_and_case"


PROMPTS = {
 State.GREETING: {
   "hi": "नमस्ते। यह साक्षी है। अपनी भाषा चुनने के लिए 1 दबाएं।",
   "kn": "ನಮಸ್ಕಾರ. ಇದು ಸಾಕ್ಷಿ. ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಲು 1 ಒತ್ತಿ.",
   "en": "Namaste. This is Saakshi. Press 1 to choose your language.",
 },
 State.MAIN_MENU: {
   "hi": ("अपनी पंचायत को मिले पैसे की जानकारी के लिए 1 दबाएं। "
          "कुछ बताने के लिए 2 दबाएं। अपने केस की स्थिति के लिए 3 दबाएं।"),
   "kn": ("ನಿಮ್ಮ ಪಂಚಾಯಿತಿಗೆ ಬಂದ ಹಣದ ಮಾಹಿತಿಗೆ 1 ಒತ್ತಿ. "
          "ಏನಾದರೂ ತಿಳಿಸಲು 2 ಒತ್ತಿ. ನಿಮ್ಮ ಪ್ರಕರಣದ ಸ್ಥಿತಿಗೆ 3 ಒತ್ತಿ."),
 },
 State.ASK_VERIFICATION: {
   "hi": ("क्या {survey_no} पर {asset} है? "
          "हाँ के लिए 1 दबाएं। नहीं के लिए 2। पता नहीं तो 3।"),
   "kn": ("{survey_no} ನಲ್ಲಿ {asset} ಇದೆಯೇ? "
          "ಹೌದು ಎಂದಾದರೆ 1 ಒತ್ತಿ. ಇಲ್ಲ ಎಂದಾದರೆ 2. ಗೊತ್ತಿಲ್ಲ ಎಂದಾದರೆ 3."),
 },
}

# ⭐ Spoken before EVERY flag disclosure. Non-negotiable. Rule R5.
UNCERTAINTY_DISCLAIMER = {
 "hi": "साक्षी छोटी चीज़ें उपग्रह से नहीं देख सकता, और साक्षी ग़लत भी हो सकता है। "
       "सच सिर्फ़ आप देख सकते हैं।",
 "kn": "ಸಾಕ್ಷಿ ಸಣ್ಣ ವಸ್ತುಗಳನ್ನು ಉಪಗ್ರಹದಿಂದ ನೋಡಲಾಗುವುದಿಲ್ಲ, ಮತ್ತು ಸಾಕ್ಷಿ ತಪ್ಪಾಗಿರಬಹುದು. "
       "ಸತ್ಯವನ್ನು ನೀವು ಮಾತ್ರ ನೋಡಬಹುದು.",
}


@router.post("/webhook")
async def ivr_webhook(CallSid: str = Form(...),
                      Digits: str | None = Form(None),
                      SpeechResult: str | None = Form(None)):
    session = await load_session(CallSid)
    twiml = await advance(session, digits=Digits, speech=SpeechResult)
    return Response(content=twiml, media_type="application/xml")
```

---

## 9. Phase 6 — PRAMAAN: citizen verification

### 9.1 Device attestation — cryptographic, not ML

```python
# src/saakshi/pramaan/attest.py
"""
Geotag authenticity.

⚠ Research found NO credible 2025-26 literature on GPS-spoof detection
  for citizen field reporting. So this is NOT an ML problem and we do
  not pretend otherwise.

⇒ Solve it CRYPTOGRAPHICALLY. Sign the capture on-device, in hardware,
  before the bytes can be touched:
    · Android Play Integrity API  (device/app integrity verdict)
    · Hardware-backed Keystore    (StrongBox where available)
    · sign(sha256(image) || lat || lon || timestamp) at capture

The server verifies the chain. An unattested photo is still ACCEPTED —
it is simply marked UNATTESTED and carries less weight. We must never
exclude a citizen for owning a cheap phone.
"""
from pydantic import BaseModel
from datetime import datetime
import hashlib


class AttestedCapture(BaseModel):
    image_sha256:   str
    lat:            float
    lon:            float
    captured_at:    datetime
    device_pubkey:  str
    signature:      str
    play_integrity_token: str | None = None


def verify(capture: AttestedCapture, image_bytes: bytes) -> dict:
    checks = {}
    checks["hash_matches"] = (
        hashlib.sha256(image_bytes).hexdigest() == capture.image_sha256)
    checks["signature_valid"] = _verify_ecdsa(
        pubkey=capture.device_pubkey,
        message=(f"{capture.image_sha256}|{capture.lat}|"
                 f"{capture.lon}|{capture.captured_at.isoformat()}").encode(),
        signature=capture.signature)
    checks["integrity_verdict"] = (
        _check_play_integrity(capture.play_integrity_token)
        if capture.play_integrity_token else "ABSENT")

    return {
        "attested": checks["hash_matches"] and checks["signature_valid"],
        "checks": checks,
        # ⭐ inclusion guarantee
        "note": ("UNATTESTED captures are still accepted with reduced "
                 "weight. A citizen is never excluded for having a "
                 "phone without hardware attestation."),
    }
```

### 9.2 Truth discovery

```python
# src/saakshi/pramaan/truth.py
"""
Multiple independent reports on one work.

arXiv:2606.28062 — LLM-based data fusion outperforms classical
unsupervised truth discovery (DART, LTM) on all three benchmarks.
arXiv:2607.24117 — weakest-link chain evaluation + independent-chain
corroboration, validated on 20,000 claims.

⚠ HONEST BOUND: reputation-weighted agreement degrades gracefully only
  within f < n/5 adversarial fraction (arXiv:2605.10370). BEYOND THAT
  IT FAILS. We state this in the docs and in the case file.
"""
from collections import Counter
from pydantic import BaseModel


class TruthVerdict(BaseModel):
    answer: str                 # yes | no | unsure | insufficient
    agreement: float
    n_reports: int
    n_independent_chains: int
    adversarial_bound_ok: bool  # ⭐ n_reports ≥ 5
    caveat: str


MIN_REPORTS = 3
MIN_AGREEMENT = 0.67


def discover(reports: list[dict]) -> TruthVerdict:
    if len(reports) < MIN_REPORTS:
        return TruthVerdict(
            answer="insufficient", agreement=0.0,
            n_reports=len(reports), n_independent_chains=0,
            adversarial_bound_ok=False,
            caveat=f"Fewer than {MIN_REPORTS} independent reports. "
                   f"A single report raises a question; it never opens a case.")

    counts = Counter(r["answer"] for r in reports)
    top, n_top = counts.most_common(1)[0]
    agreement = n_top / len(reports)
    chains = len({r["anon_commitment"] for r in reports})

    return TruthVerdict(
        answer=top if agreement >= MIN_AGREEMENT else "unsure",
        agreement=agreement,
        n_reports=len(reports),
        n_independent_chains=chains,
        adversarial_bound_ok=len(reports) >= 5,
        caveat=("Truth discovery is reliable only while adversarial "
                "reporters are fewer than 1 in 5. With "
                f"{len(reports)} reports this bound is "
                f"{'satisfied' if len(reports) >= 5 else 'NOT YET satisfied'}."),
    )
```

### 9.3 Anonymity — and an honest scope note

```python
# src/saakshi/pramaan/anon.py
"""
Sybil resistance WITHOUT identifying the reporter.

TWO PROVED IMPOSSIBILITIES bound this:
  · No voting rule deriving power solely from a splittable resource
    resists Sybil splitting on a permissionless system. Replaying 10
    proposals across 5 major DAOs showed Sybil amplification of
    1,172×-4,039× EVEN UNDER QUADRATIC VOTING   (arXiv:2605.18990)
  · Exact Shapley-fair attribution over reported identities is
    INCOMPATIBLE with unrestricted false-name-proofness (arXiv:2605.07663)

⇒ The ONLY construction that works needs an EXTERNAL IDENTITY ANCHOR.
  DARTIC (arXiv:2605.18146) binds all pseudonyms to one access token
  via zkSNARK set-membership: proof gen <3 s; batched verification of
  1024 proofs drops 8.7 s → 0.96 s.

SAAKSHI's anchor: the PHONE NUMBER. Bound once via OTP, then discarded
into a commitment. One phone, one voice — and the government CANNOT
link a report to a caller.

  ⭐ WHY THIS IS NOT OPTIONAL: nobody reports the patwari to the
     patwari. If the local official can learn who called, nobody calls.

⚠ HACKATHON SCOPE HONESTY: the full zkSNARK circuit is a PROOF OF
  CONCEPT in this submission. The shipped path uses a blinded
  commitment + server-side nullifier set, which gives unlinkability
  against a passive server but NOT against a colluding operator. The
  circuit design and the migration path are documented; the production
  guarantee is NOT claimed. SAY THIS ON THE SLIDE.
"""
import hashlib, secrets


def enroll(phone_e164: str, system_salt: bytes) -> tuple[str, str]:
    """
    Returns (commitment, nullifier_seed).
    The phone number is used ONCE and never persisted.
    """
    blinding = secrets.token_bytes(32)
    commitment = hashlib.blake2b(
        phone_e164.encode() + blinding, key=system_salt, digest_size=32
    ).hexdigest()
    nullifier_seed = hashlib.blake2b(blinding, digest_size=32).hexdigest()
    return commitment, nullifier_seed
    # phone_e164 goes out of scope here and is never written to disk.
```

### 9.4 ⭐ The novel loop: reports → training labels

```python
# src/saakshi/pramaan/labels.py
"""
⭐⭐ THE RESEARCH CONTRIBUTION (Novelty Gap N2) ⭐⭐

Verified citizen reports become POSITIVE-UNLABELED training labels for
the Layer-1 network model.

WHY THIS MATTERS: arXiv:2512.19491 identifies the structural blocker in
ALL procurement-fraud ML — THERE ARE NO CONFIRMED POSITIVES. Sanction
records are the only ground truth anyone has, and they are rare and
arrive years late.

Crowdsourcing-integrity work treats reports as the END PRODUCT.
Graph fraud detection treats labels as EXOGENOUS.
Clue2Group (arXiv:2606.26189) comes closest but assumes a PROFESSIONAL
ANALYST, not a villager.

NOBODY HAS PUBLISHED THIS LOOP.

The flywheel: more reports → better model → better-targeted questions
→ more useful reports.
"""
from pydantic import BaseModel


class PULabel(BaseModel):
    vendor_id: str
    work_id: str
    label: int                  # 1 = confirmed positive. NEVER 0.
    source: str                 # "citizen_verified" | "cag" | "cvc" | "cci"
    confidence: float
    n_reports: int
    corroborating_signals: list[str]


PROMOTION_RULE = """
A citizen report becomes a PU POSITIVE only when ALL hold:
  1. truth-discovery answer == "no" (asset absent)
  2. agreement >= 0.67
  3. n_reports >= 3 from independent anon commitments
  4. ⭐ at least ONE independent MACHINE signal also fired
     (photo duplicate | payment anomaly | satellite no-change)
  5. adversarial bound satisfied (n_reports >= 5) OR a human reviewer
     has adjudicated

Rule 4 is the safeguard: citizen reports NEVER become labels on their
own. Machine and human must agree. This prevents a coordinated
political brigade from poisoning the model.
"""


def promote(verdict, bundle, vendor_id: str) -> PULabel | None:
    if verdict.answer != "no":                       return None
    if verdict.agreement < 0.67:                     return None
    if verdict.n_independent_chains < 3:             return None

    machine = [s.detector for s in bundle.signals
               if s.fired and s.detector != "citizen"]
    if not machine:                                  return None   # rule 4

    return PULabel(
        vendor_id=vendor_id, work_id=bundle.work_id, label=1,
        source="citizen_verified",
        confidence=min(verdict.agreement, 0.95),
        n_reports=verdict.n_reports,
        corroborating_signals=machine,
    )
```

---

## 10. Phase 7 — GHADI: the accountability clock

```python
# src/saakshi/ghadi/casefile.py
"""
The case file.

THE VOID THIS FILLS: AuditOnline reports 62,745 observations and ZERO
Action Taken Reports, nationally. Recovery on detected MGNREGA
misappropriation is UNDER 13%.

Finding fraud is not the hard part. India already finds ~₹200 crore a
year and recovers ~₹20 crore.

Architecture per arXiv:2607.19266 (graph features → explanations →
agentic case file), with citation validity as a first-class metric
(arXiv:2604.19755: 0.98 citation validity, 0.88 evidence support).
"""
from datetime import date, timedelta
from pydantic import BaseModel, Field
from typing import Literal


class StatutoryClock(BaseModel):
    instrument: Literal["RTI_6_1", "CPGRAMS", "GRAM_SABHA"]
    filed_on: date
    statutory_days: int
    reference_no: str | None = None

    @property
    def deadline(self) -> date:
        return self.filed_on + timedelta(days=self.statutory_days)

    @property
    def days_remaining(self) -> int:
        return (self.deadline - date.today()).days

    @property
    def breached(self) -> bool:
        return self.days_remaining < 0


STATUTORY_DAYS = {
    "RTI_6_1":  30,   # RTI Act 2005 §7(1)
    "CPGRAMS":  21,   # Comprehensive Guidelines, 23 August 2024
    "GRAM_SABHA": 90, # next statutory sitting
}


class CaseFile(BaseModel):
    case_id: str
    work_id: str
    gp_code: int
    opened_on: date
    status: Literal["OPEN", "AWAITING_RESPONSE", "RESPONDED",
                    "ESCALATED", "RESOLVED", "RECOVERED", "CLOSED_NO_ACTION"]

    signals: list[dict]
    unknowns: list[str] = Field(min_length=1)   # ⭐ can NEVER be empty
    clocks: list[StatutoryClock]

    responsible_designation: str   # ⭐ DESIGNATION ONLY, never a name
    amount_involved: float
    amount_recovered: float = 0.0

    @property
    def is_verdict(self) -> bool:
        return False   # ⭐ structurally. A case file is a QUESTION.
```

```python
# src/saakshi/ghadi/rti.py
"""
RTI §6(1) draft generator.

⭐ THE KEY INSIGHT: a GENERIC RTI gets refused for vagueness.
   A SPECIFIC one, citing exact document IDs and dates, CANNOT.

SAAKSHI already knows the work ID, the sanction order date, the FTO
number, the muster roll reference and the photo IDs — because it
scraped them. So it drafts an RTI that is impossible to deflect.
"""
TEMPLATE = """\
To,
The Public Information Officer,
{department}
{address}

Subject: Application under Section 6(1) of the Right to Information
         Act, 2005

Sir/Madam,

I request the following information regarding Work ID {work_id}
({work_name}) in Gram Panchayat {gp_name}, Block {block_name},
District {district_name}, {state_name} (LGD code {gp_code}):

1. Certified copy of the Administrative Approval / Technical Sanction
   for the above work, sanctioned on {sanction_date} for
   ₹{sanctioned_amount:,.0f}.

2. Certified copies of all muster rolls generated for the said work
   between {sanction_date} and {claimed_completion_date}.

3. Certified copies of all Fund Transfer Orders (FTOs) and payment
   vouchers issued against the said work, including FTO numbers
   {fto_list}.

4. Certified copies of the measurement book entries recorded for the
   said work.

5. The date on which the said work was physically verified by the
   Junior Engineer / Technical Assistant, and the name and designation
   of the officer who conducted the verification.

6. Certified copies of the geo-tagged photographs uploaded against
   the said work at each stage, together with the date, time and
   device identifier of upload for each photograph.

7. The Utilisation Certificate submitted for the said work.

8. If the said work has been reported as completed, the date of
   completion certification and the designation of the certifying
   officer.

I am a citizen of India. The application fee of ₹10 is enclosed /
has been paid vide {fee_reference}.

I request that the information be provided within 30 days as mandated
under Section 7(1) of the Act.

Yours faithfully,
{applicant_name}
{applicant_address}
Date: {today}

---
Prepared with SAAKSHI (saakshi.org.in) · Case {case_id}
This application cites specific, verifiable document identifiers
obtained from public government portals.
"""
```

**Expected output — the public case page:** see §12.3.

---

## 11. Phase 8 — The killer demo

### ⭐ Retrospective validation against CAG's own published findings

**This is what wins.** Do not demo on synthetic data. Do not demo on a hypothetical village.

> **The demo claim:**
>
> *"We are not claiming to find new fraud. We are proving we can automatically re-derive fraud that CAG needed a months-long manual audit to find — from the same public data, in seven minutes, at national scale instead of a 39-panchayat sample."*

That claim is verifiable, falsifiable, and impossible to dismiss.

**The ground truth file:**

```yaml
# data/ground_truth/cag_karnataka_2026.yaml
# CAG performance audit, MGNREGA Karnataka, FY2019-20 to FY2023-24,
# tabled 24 March 2026.
#
# ⚠ SOURCING: headline findings corroborated by Deccan Herald
#   (24 Mar 2026). Granular sub-figures reported by Organiser
#   (7 Apr 2026), an RSS-affiliated outlet — flagged as REQUIRING
#   CONFIRMATION against the CAG PDF. See RESEARCH.md §A1.3.
#   We do NOT present unconfirmed sub-figures as established fact.

source: "CAG Performance Audit, MGNREGA Karnataka, tabled 2026-03-24"
confidence: "headline=corroborated; granular=requires_confirmation"

findings:
  - id: CAG-KA-01
    type: duplicate_photographs
    description: "Identical photographs uploaded across different
                  construction stages to fake progress"
    detector: photos.find_duplicates
    expect: "≥1 cross-stage pHash match within the sampled works"

  - id: CAG-KA-02
    type: stage_payment_after_completion
    count: 462
    description: "Payments for foundation/lintel/roofing on houses
                  already completed earlier"
    detector: payments.temporal_impossibility
    expect: "count within ±10% of 462 on the same sample frame"

  - id: CAG-KA-03
    type: no_work_executed
    count: 12
    description: "No work executed at all, yet payments processed.
                  Detected by CAG using Google Earth historical data."
    detector: satellite.verify_work
    expect: "no-change flag on ≥8 of 12 (satellite-verifiable subset only)"

  - id: CAG-KA-04
    type: threshold_splitting
    location: "Koppal, Yelburga taluk"
    description: "Check dam split into two smaller works to bypass
                  tendering; >₹10 lakh paid without verification"
    detector: payments.threshold_splitting
    expect: "sibling-group flag on the Yelburga check-dam works"

  - id: CAG-KA-05
    type: ghost_workers
    metric: "~40% average active-worker share ⇒ ~60% never worked"
    detector: naammilan.resolve
    expect: "duplicate-cluster rate materially above the state baseline"

  - id: CAG-KA-06
    type: post_completion_procurement
    location: "Kalaburagi, Kamalapur taluk — solid waste shed"
    description: "Materials shown as purchased AFTER project completion;
                  muster rolls, bills and geo-tagged images tampered"
    detector: payments.temporal_impossibility
    expect: "flag on the Kamalapur solid-waste-shed work"
```

**The demo runner:**

```python
# notebooks/01_cag_retrospective.ipynb  (or scripts/demo.py)
"""
SAAKSHI — CAG Retrospective Validation

Runs all four detectors over the same public data CAG audited, and
scores our automated findings against CAG's manual findings.
"""
import yaml, time
from rich.console import Console
from rich.table import Table

console = Console()
gt = yaml.safe_load(open("data/ground_truth/cag_karnataka_2026.yaml"))

console.rule("[bold]SAAKSHI · CAG RETROSPECTIVE VALIDATION")
console.print(
    "[dim]CAG audited 39 gram panchayats and 847 projects by hand.\n"
    "SAAKSHI runs the same four checks over the full public corpus.[/dim]\n")

t0 = time.time()
results = run_all_detectors(scope="karnataka", fy="2023-24")
elapsed = time.time() - t0

tbl = Table(title="CAG finding  vs  SAAKSHI automated detection")
tbl.add_column("CAG ID");   tbl.add_column("Finding")
tbl.add_column("CAG");      tbl.add_column("SAAKSHI")
tbl.add_column("Match")

for f in gt["findings"]:
    ours = results[f["detector"]]
    tbl.add_row(f["id"], f["type"],
                str(f.get("count", "qualitative")),
                str(ours.count), "✓" if ours.matches(f) else "✗")
console.print(tbl)

console.print(f"\n[bold green]CAG: months of manual audit, "
              f"39 panchayats, 847 projects.")
console.print(f"[bold green]SAAKSHI: {elapsed:.0f} seconds, "
              f"full state corpus.[/bold green]")
```

**Expected demo output:**

```
════════ SAAKSHI · CAG RETROSPECTIVE VALIDATION ════════
CAG audited 39 gram panchayats and 847 projects by hand.
SAAKSHI runs the same four checks over the full public corpus.

        CAG finding  vs  SAAKSHI automated detection
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ CAG ID    ┃ Finding                  ┃ CAG   ┃ SAAKSHI ┃ Match ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ CAG-KA-01 │ duplicate_photographs    │ qual. │      47 │   ✓   │
│ CAG-KA-02 │ stage_pmt_after_complete │   462 │     462 │   ✓   │
│ CAG-KA-03 │ no_work_executed         │    12 │       9 │   ✓   │
│ CAG-KA-04 │ threshold_splitting      │ qual. │       1 │   ✓   │
│ CAG-KA-05 │ ghost_workers            │  qual │  3.1× σ │   ✓   │
│ CAG-KA-06 │ post_completion_procure  │ qual. │       1 │   ✓   │
└───────────┴──────────────────────────┴───────┴─────────┴───────┘

⚠ CAG-KA-03: 9 of 12, not 12 of 12. Three works were toilets and
  single houses — BELOW the 10 m Sentinel-2 detection limit. SAAKSHI
  correctly REFUSED to analyse them and routed them to citizen
  verification. This is the honesty gate working as designed.

CAG: months of manual audit, 39 panchayats, 847 projects.
SAAKSHI: 441 seconds, full state corpus.
```

> **That `⚠ 9 of 12, not 12 of 12` line is worth more than a perfect score.** It shows the honesty gate firing correctly, it explains a miss with physics rather than excuses, and it demonstrates the system knows what it cannot do. **Leave it in. Lead with it in Q&A.**

---

## 12. OUTPUT SPECIFICATIONS — what everything looks like

### 12.1 CLI

```powershell
make ingest      # pull all portals into data/raw + warehouse.duckdb
make graph       # build kosh.kuzu from the warehouse
make detect      # run all four detectors, write evidence bundles
make resolve     # entity resolution
make cases       # open case files, draft RTI/CPGRAMS, start clocks
make serve       # FastAPI on :8000
make demo        # ⭐ the CAG retrospective validation
```

### 12.2 Public dashboard — landing page

```
┌────────────────────────────────────────────────────────────────────┐
│  साक्षी  SAAKSHI                    [हिंदी ▾]  [Search a village…] │
│  The witness for every rupee.                                      │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│    ☎  1800-XXX-SAAKSHI                                             │
│       Call free, in your language, to hear what your               │
│       panchayat was paid. No smartphone needed.                    │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│  WHAT INDIA ALREADY KNOWS                                          │
│                                                                    │
│    ₹1,000 cr+     detected by MGNREGA social audits, 6 years       │
│    ₹122.66 cr     recovered                          ▓░░░░░ 12.6%  │
│    ₹878 cr        untraced                                         │
│                                                                    │
│    62,745         audit observations recorded on AuditOnline       │
│    0              Action Taken Reports generated       ← nationally│
│                                                                    │
│    38.58%         of panchayats audited in FY2025-26               │
│    61,347         cases found in that 38.58%                       │
├────────────────────────────────────────────────────────────────────┤
│  WHAT SAAKSHI FOUND        [Karnataka ▾]   [FY 2026-27 ▾]          │
│                                                                    │
│   Works screened ............................. 14,203              │
│   Duplicate completion photos ................  1,284  ⚠           │
│   Stage payments after completion .............   462  ⚠           │
│   Threshold-splitting sibling groups ..........    34  ⚠           │
│   Satellite: no change at claimed site ........   469  ⚠           │
│   Skipped — below satellite detection limit ...  9,118  ← honest    │
│                                                                    │
│   Open cases ..................................   211              │
│   Awaiting government response ................   188              │
│   ⏱ Statutory deadline breached ...............    41  ⚠           │
├────────────────────────────────────────────────────────────────────┤
│  ⭐ INDIA'S SINGLE-BID TENDER RATE   (first published computation)  │
│                                                                    │
│   All CPPP entities (n=97,884 tenders) ............  XX.X%         │
│   Worst 5 procuring entities:                                      │
│     RDPR::Koppal::Yelburga ......................... 68.8%  ⚠      │
│     RDPR::Kalaburagi::Kamalapur .................... 52.2%  ⚠      │
│     …                                                              │
│                                                    [Full table →]  │
└────────────────────────────────────────────────────────────────────┘
```

### 12.3 Public case page

```
┌────────────────────────────────────────────────────────────────────┐
│  CASE KA-KLB-2026-00412                    ⏱ 15 DAYS REMAINING     │
├────────────────────────────────────────────────────────────────────┤
│  Farm pond · Survey no. 112/3                                      │
│  Kamalapur GP, Kalaburagi, Karnataka · LGD 226534                  │
│                                                                    │
│  Scheme MGNREGA │ Sanctioned ₹4,20,000 on 12 Mar 2026              │
│  Claimed completed 14 Jun 2026 │ Case opened 14 Jul 2026           │
├────────────────────────────────────────────────────────────────────┤
│  FOUR INDEPENDENT SIGNALS                                          │
│  (deliberately NOT combined into a single score — red flags are    │
│   multidimensional and non-superimposable, arXiv:2309.01462)       │
│                                                                    │
│  ① PHOTO FORENSIC                            confidence: HIGH ▓▓▓  │
│     The completion photo is pHash-identical (Hamming 0/64) to      │
│     the completion photo of work KA-KOP-2026-00189 in Yelburga     │
│     — 61.3 km away.                                                │
│     method: perceptual hash · deterministic · reproducible         │
│     limitation: a duplicate may be an upload error, not fraud      │
│     evidence: [nmms_88213.jpg] [nmms_71104.jpg]                    │
│                                                                    │
│  ② SATELLITE                                  confidence: LOW ▓░░  │
│     Sentinel-2, 08 Mar 2026 vs 19 Jun 2026. NDWI Δ = +0.012        │
│     (threshold +0.10). No detectable surface-water feature.        │
│     limitation: ⚠ 10 m GSD = 100 m² per pixel. Small ponds may     │
│                 fall BELOW the detection limit. NOT DISPOSITIVE.   │
│     evidence: [before.tif] [after.tif] [side-by-side ↗]            │
│                                                                    │
│  ③ NETWORK                                  confidence: MEDIUM ▓▓░ │
│     The contracted vendor won 11 of 16 block tenders as the sole   │
│     bidder (block median: 0). Award/estimate +2.1% vs block        │
│     median −8.4%.                                                  │
│     method: LightGBM on graph features, PU-calibrated (c=0.31)     │
│     limitation: sole bidding may reflect a genuine absence of      │
│                 local contractors, not collusion                   │
│     evidence: [CPPP award list ↗]                                  │
│                                                                    │
│  ④ CITIZEN VERIFICATION                      confidence: HIGH ▓▓▓  │
│     3 independent anonymous reports: "no pond at this location."   │
│     agreement 1.00 · independent chains 3                          │
│     limitation: ⚠ truth discovery is reliable only while           │
│                 adversarial reporters are fewer than 1 in 5.       │
│                 With 3 reports this bound is NOT YET satisfied.    │
│     reports: pramaan_a91f2 · pramaan_c04e8 · pramaan_7b331         │
│              (anonymous — not linkable to any caller)              │
├────────────────────────────────────────────────────────────────────┤
│  ⚠ WHAT WE DO NOT KNOW                                             │
│    • Whether the pond exists but is below satellite resolution     │
│    • Whether the duplicate photo is fraud or an upload error       │
│    • Whether sole bidding reflects collusion or no local bidders   │
│                                                                    │
│    THIS CASE FILE IS A QUESTION, NOT A VERDICT.                    │
├────────────────────────────────────────────────────────────────────┤
│  ⏱ THE CLOCK                                                       │
│                                                                    │
│   RTI §6(1) ......... filed 14 Jul 2026  →  due 13 Aug   15 days ▓▓│
│   CPGRAMS ........... filed 14 Jul 2026  →  due 04 Aug    6 days ▓ │
│                       ref CPGRAMS/2026/0412773                     │
│   Gram Sabha ........ queued for next statutory sitting            │
│                                                                    │
│   Responsible office: Programme Officer, Kamalapur Block           │
│   (designation only — SAAKSHI never names an individual)           │
│                                                                    │
│   [Download RTI PDF]  [Download full evidence pack]  [Subscribe]   │
└────────────────────────────────────────────────────────────────────┘
```

### 12.4 The Recovery Ledger

```
┌────────────────────────────────────────────────────────────────────┐
│  RECOVERY LEDGER · who actually gets the money back                │
│  ⭐ Nobody currently publishes this. Source: NREGASoft R 9.2.6      │
├────────────────────────────────────────────────────────────────────┤
│  district        detected     recovered    rate    cases  breached │
│  ─────────────────────────────────────────────────────────────────│
│  Kalaburagi      ₹4.41 cr     ₹0.39 cr     8.8%      412      104  │
│  Koppal          ₹2.18 cr     ₹0.11 cr     5.0%      188       71  │
│  Ballari         ₹3.02 cr     ₹0.84 cr    27.8%      301       22  │
│  ─────────────────────────────────────────────────────────────────│
│  KARNATAKA      ₹44.18 cr     ₹3.90 cr     8.8%    4,412    1,204  │
│  NATIONAL     ₹1,000+ cr    ₹122.66 cr    12.6%       —        —   │
│                                                                    │
│  ▸ Ballari recovers 3× better than Koppal on comparable volume.    │
│    Nobody has been able to see this before.                        │
└────────────────────────────────────────────────────────────────────┘
```

### 12.5 API contract

```python
# GET /api/v1/panchayat/{gp_code}/summary?fy=2026-27
{
  "panchayat": {"gp_code": 226534, "gp_name": "Kamalapur",
                "block": "Kamalapur", "district": "Kalaburagi",
                "state": "Karnataka"},
  "fiscal_year": "2026-27",
  "totals": {"works": 14, "sanctioned": 4_712_000.0,
             "completed": 11, "schemes": ["MGNREGA", "PMAY-G", "SBM-G"]},
  "flags": {"works_with_signals": 2, "open_cases": 1},
  "provenance": [
    {"source_portal": "NREGASoft",
     "source_url": "https://mnregaweb4.nic.in/netnrega/...",
     "fetched_at": "2026-07-29T02:14:33Z",
     "content_sha256": "9f2a...", "parser_version": "1.0"}
  ],
  "disclaimer": "SAAKSHI reports questions, not verdicts. Satellite "
                "verification is limited to assets larger than the 10 m "
                "Sentinel-2 detection limit."
}
```

```python
# GET /api/v1/case/{case_id}   → the CaseFile model verbatim
# GET /api/v1/redflags/single-bid-rate?level=block&state=KA
# POST /api/v1/report          → citizen report (anon commitment required)
# POST /ivr/webhook            → telephony
```

---

## 13. Testing strategy

| Layer | Test | Why |
|---|---|---|
| **Ingest** | `pytest-vcr` cassettes per portal | CI must run offline. Government portals go down |
| **Ingest** | Schema-drift canary — assert expected columns, fail loudly | Government HTML changes without notice |
| **Provenance** | Property test: **no `Fact` can be constructed without valid `Provenance`** | R4 enforcement |
| **Queries** | Every `.cypher` has a golden-result test on a fixture graph | R2. A broken query is a wrong answer to a citizen |
| **Intent router** | Assert `UnknownIntent` raised for any unregistered name | R2 |
| **Intent router** | Adversarial set: 100 questions incl. **20 unanswerable**. Assert `UNKNOWN` on all 20 | arXiv:2607.25243 — open models *never abstain*. We must |
| **pHash** | Known-duplicate fixture pairs + hard negatives (same site, different day) | False positives here open wrong cases |
| **Satellite** | Assert honesty gate **refuses** `toilet`, `hand_pump`, `soak_pit` | The gate is the ethic |
| **Payments** | Assert temporal check reproduces **462** on the CAG fixture | The validation claim |
| **ER** | Assert posteriors emitted, **never a binary verdict** | Exclusion-error prevention |
| **Truth discovery** | Assert `insufficient` below 3 reports; assert bound warning below 5 | Adversarial bound |
| **PU labels** | Assert rule 4 — **no citizen-only label ever promotes** | Anti-brigading |
| **Case file** | Assert `unknowns` is non-empty; assert `is_verdict is False` | Legal posture |
| **Case file** | Assert no field ever contains an individual's name | Defamation |
| **E2E** | `make demo` runs green in CI | If a judge can't run it, it's a mockup |

---

## 14. Build order and timeline

**Build the demo-critical path first.** Voice and ER are what make it *inclusive*; photo + satellite + case file are what make it *believable*. You need both, in that order.

| Stage | What | Ships |
|---|---|---|
| **1** | LGD loader → DuckDB → Kuzu skeleton | The spine. Nothing works without it |
| **2** | CPPP connector + `red_flags_by_entity` | **India's first single-bid rate.** A standalone publishable artefact on day one |
| **3** | Photo forensics (pHash + EXIF + device itinerary) | **Highest value per line.** The CAG duplicate-photo finding, automated |
| **4** | Payment detectors (threshold split + temporal) | The **462**. The validation claim |
| **5** | Satellite + the honesty gate | The Google-Earth-by-hand replacement, with its limits stated |
| **6** | Evidence bundle + case file + RTI generator + clock | The **0 ATRs** answer |
| **7** | `make demo` — CAG retrospective | **The thing that wins** |
| **8** | Public dashboard (Jinja + HTMX + Leaflet) | What a judge clicks |
| **9** | NREGASoft connector (Playwright) | Hardest ingest. Deliberately late — everything else works without it |
| **10** | VAANI: intent router + IVR state machine + Bhashini | The inclusion layer |
| **11** | NAAM-MILAN entity resolution | Ghosts |
| **12** | PRAMAAN: attestation + truth discovery + PU loop | The research contribution |
| **13** | Docs, architecture diagram, README, demo video | Presentation marks are real marks |

> **If time runs out, ship stages 1–8.** That is a complete, demonstrable, honest system with a validated novel finding. Stages 10–12 can be a documented roadmap with a working single-language IVR prototype — and you say so, clearly, rather than faking it.

---

## 15. Submission deliverables checklist

Mapped directly to the required sections in `about.txt`:

| Required section | Deliverable | Source |
|---|---|---|
| **1. Problem Statement Identification** | `idea.md` §2–4, `RESEARCH.md` Part A | ✅ |
| **2. Solution Overview, Innovation & Differentiation** | `idea.md` §6–9 + the six novelty gaps | ✅ |
| **3. Technology or Implementation Framework** | This file + `docs/architecture.excalidraw` | ✅ |
| **4. Prototype / Pilot Details** | `make demo` — CAG retrospective validation + demo video | ⬜ build |
| **5. Scalability & Sustainability Plan** | `idea.md` §13 | ✅ |
| **6. Expected Social & Economic Impact** | `idea.md` §12 | ✅ |
| **7. Team Information** | — | ⬜ fill in |
| **8. Supporting Documents** | `RESEARCH.md`, evidence pack PDF, screenshots | ✅ |

**Also required by the hackathon:**

- ⬜ **Application form** — download from the TechGig page and attach
- ✅ **MIT LICENSE** file in repo root
- ⬜ **Demo video** — screen recording of `make demo`, ≤3 minutes
- ⬜ **Presentation deck** — the narrative arc below
- ⬜ **Team: Indian nationals, 18+ as on 30 May 2026, 2–4 members**

### The deck narrative (10 slides)

| # | Slide | The beat |
|---|---|---|
| 1 | **The auditor opened Google Earth** | The CAG Karnataka story. Four manual detection methods |
| 2 | **All four are batch jobs** | The table. pHash, raster diff, GROUP BY, date comparison |
| 3 | **62,745 observations. 0 ATRs.** | The live AuditOnline screenshot. Under 13% recovered |
| 4 | **The data is public. The join key exists.** | LGD mandated since 4 Nov 2016. 255,297 GPs. Nobody has joined it |
| 5 | **SAAKSHI** | The six layers, one diagram |
| 6 | **⭐ Live demo** | `make demo`. CAG's 462 → our 462 |
| 7 | **What we cannot do** | The honesty gate. 10 m GSD. 64% of works skipped. **This slide earns trust** |
| 8 | **☎ Meet Lakshmi** | The 100-second call. 48.4%. No app. No literacy. No English |
| 9 | **The loop nobody has published** | Citizen reports → PU labels → better model. The flywheel |
| 10 | **₹878 crore is untraced. Both halves are engineering problems.** | The ask |

---

## 16. Known risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| **NREGASoft blocks the crawler** | High | Two strategies (httpx + Playwright); polite rate limits; **stages 1–8 do not depend on it**; LibTech proved 31.36M transactions is achievable |
| **Government HTML changes mid-build** | High | Schema-drift canaries fail loudly; VCR cassettes keep CI green; raw HTML archived in `data/raw/` |
| **Sentinel-2 cloud cover in monsoon** | High | ±30-day search window; fall back to Landsat 30 m; **report "no cloud-free scene" honestly rather than guessing** |
| **False positives open wrong cases** | Medium | Two-signal + one-HIGH-confidence rule; mandatory `unknowns` section; posteriors not verdicts; **case files are questions** |
| **Bhashini API access / quota** | Medium | IndicConformer local fallback; DTMF-only mode works with **zero ASR** |
| **zkSNARK complexity blows the timeline** | Medium | **Already scoped as PoC.** Blinded commitment + nullifier set ships; the production guarantee is documented as future work and **not claimed** |
| **A judge asks "isn't this Aadhaar-seeding again?"** | High | Rehearse the architectural answer: read-only, post-hoc, no authority to deny. **A false positive costs an official an explanation; it never costs a citizen their rice** |
| **A judge asks "can satellites really see a toilet?"** | High | **Answer it before they ask it, on slide 7.** 10 m GSD, IoU ≈ 4% built-up, 64% skip rate |
| **Scope creep across six layers** | **Very high** | **Stages 1–8 are the submission. 10–12 are the roadmap.** Decide this on day one and hold it |

---

## Appendix — every data source, in one table

| Source | URL | Access | Status |
|---|---|---|---|
| **LGD** ⭐ | `lgdirectory.gov.in` | Bulk download + NAPIX API | ✅ open |
| CPPP | `eprocure.gov.in/cppp` | Public HTML, incl. `/resultoftendersnew` | ✅ open |
| AuditOnline | `auditonline.gov.in` | Citizen Section, PDF + Excel | ✅ open |
| eGramSwaraj | `egramswaraj.gov.in` | Dashboards + published API spec | ✅ open |
| CPGRAMS | `pgportal.gov.in/darpgdashboard` | Public HTML table | ✅ open |
| DBT Bharat | `dbtbharat.gov.in` | HTML | ✅ open |
| IMPDS / ONORC | `impds.nic.in` | Export to Excel | ✅ open |
| GeM | `gem.gov.in` · `bidplus.gem.gov.in/all-bids` | Counters + bid list | ✅ open |
| API Setu | `apisetu.gov.in` | 8,900+ REST APIs | ✅ open |
| data.gov.in | `data.gov.in` | GODL-India | ✅ open |
| **NREGASoft** | `nrega.nic.in` · `mnregaweb4.nic.in` | ⚠ session-aware crawl required | ⚠ awkward |
| CAG | `cag.gov.in` | PDFs only, untagged | ⚠ awkward |
| CVC | `cvc.gov.in/annualreport` | PDFs only, 1986–2024 | ⚠ awkward |
| **Sentinel-2 L2A** | `earth-search.aws.element84.com/v1` | STAC, COG, **no auth** | ✅ free |
| Landsat 8/9 | USGS | 30 m, 16-day | ✅ free |
| Bhuvan / ISRO | `bhuvan.nrsc.gov.in` | Browse + thematic layers | ✅ free |
| **PFMS** | `pfms.nic.in` | **Login-gated** | ❌ **out of scope** |

---

*Idea: `idea.md`. Evidence: `RESEARCH.md`. Build: this file.*

> **Chitragupta keeps the ledger. Saakshi bears witness. Bharat asks the question.**
