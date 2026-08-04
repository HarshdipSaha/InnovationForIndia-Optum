# SAAKSHI (साक्षी) — the witness for every rupee

> A read-only forensic and accountability layer over India's public spending data —
> and a toll-free phone number that lets any citizen interrogate it in their own language.
>
> **TechGig × Optum — Inclusive Innovation for Bharat · Theme 05 (GovTech & Public Service Delivery)**
> **License: MIT**

This repository is the hackathon **prototype**: the demo-critical path from
[`../PLAN.md`](../PLAN.md) — photo forensics + payment forensics + procurement
red flags + the accountability case file — running as a **retrospective
validation** against the March 2026 CAG Karnataka MGNREGA performance audit.

The idea, the full build plan, and the evidence base live one directory up:
[`idea.md`](../idea.md) · [`PLAN.md`](../PLAN.md) · [`RESEARCH.md`](../RESEARCH.md).

---

## 60-second quickstart

```bash
python run_demo.py                    # runs every detector + prints the case file
python -m unittest discover -s tests  # 10 tests, zero dependencies
```

**No `pip install`. No network. No API keys.** The demo runs on the Python
standard library alone (Python 3.11+). A judge can clone and run it in one
command — which is the whole point: *a judge who cannot run your prototype scores
your prototype as a mockup.*

The production stack in `PLAN.md` (DuckDB, KùzuDB, imagehash, rasterio, LightGBM,
splink, FastAPI …) is declared as an optional extra in `pyproject.toml` and is
**not required** to run this retrospective demo.

---

## What the demo proves

It reconstructs the CAG Karnataka findings as a synthetic dataset, then shows
SAAKSHI's detectors **independently re-deriving each one** from scratch:

| CAG found, by hand, in a 39-panchayat sample | SAAKSHI detector | Result |
|---|---|---|
| Identical photos reused across construction stages | perceptual hash (dHash) | reused completion photo found, **Hamming 0/64**, across two works **61 km** apart in different districts |
| Payments for stages on already-completed houses | temporal consistency (a date comparison) | **462 instances · ₹1.19 crore · MATCH → VALIDATED** |
| A check dam split in two to dodge tendering | threshold-split detection | ₹2.4L + ₹2.9L = **₹5.3L** crossing the ₹5L limit, same GP + vendor, 11 days apart |
| (world-standard indicator India never publishes) | single-bid rate + repeat-winner HHI | **India's first single-bid-rate table**; one vendor won **11 of its tenders as the sole bidder** |
| — | impossible-itinerary check | one device geo-tagging attendance at **8 sites in under an hour** |

All five checks are asserted in the demo (`run_demo.py` exits non-zero if any
fails) and in the test suite.

> **Integrity note.** The bundled dataset is a **synthetic reconstruction** of
> published CAG findings, not live-scraped portal data. Live ingest (KOSH) crawls
> the real public portals and is out of scope for a zero-network demo. Everything
> the demo labels "VALIDATED" is a detector rediscovering a structure that was
> deliberately seeded to match a published CAG number. See
> [`data/ground_truth/cag_karnataka_2026.json`](data/ground_truth/cag_karnataka_2026.json).

---

## Design rules enforced in code

- **R1 — determinism for anything a citizen sees.** Perceptual hashes, date
  comparisons and `GROUP BY`s only on the citizen-facing path. dHash and the
  generator are deterministic (tested).
- **R2 — no LLM ever writes a query.** (Production: an intent router over ~40
  vetted parameterised queries. Not exercised in this offline demo.)
- **R4 — every fact carries provenance.** See `src/saakshi/common/provenance.py`.
- **R5 — ship the honest limit with the capability.** The satellite signal is
  scoped to large assets and carries a "10 m GSD · NOT dispositive" caveat; the
  case file always includes a **"What we do not know"** section and states, in
  writing, that it is *a question, not a verdict*. No single fused "corruption
  score" is ever emitted (tested).

---

## Layout

```
saakshi/
├── run_demo.py                    # entry point
├── pyproject.toml                 # deps = []  (prod stack is an optional extra)
├── LICENSE                        # MIT
├── data/ground_truth/             # the CAG validation anchors
├── docs/DEMO_OUTPUT.txt           # captured output of a demo run
├── src/saakshi/
│   ├── common/{provenance,models}.py
│   ├── synth/generate.py          # deterministic CAG-retrospective dataset
│   ├── chitragupta/{photos,payments,network}.py   # the detectors
│   ├── ghadi/casefile.py          # the accountability case file + RTI draft
│   └── demo/report.py             # orchestration + validation
└── tests/test_detectors.py        # 10 tests, stdlib unittest
```

## Scraping ethics (applies to the production ingest layer)

Every source SAAKSHI uses is published by the Government of India for public
consumption. Even so, the ingest layer must: respect `robots.txt`; rate-limit to
1 request / 2 s; identify itself honestly in the `User-Agent`; cache aggressively;
and never touch anything behind authentication (PFMS is login-gated → out of
scope). This demo makes **no network requests at all**.
