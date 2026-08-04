# RESEARCH.md — Everything, From Scratch

**Compiled:** 29 July 2026
**For:** TechGig × Optum — *Inclusive Innovation for Bharat*
**Track chosen:** Theme 05 — **GovTech & Public Service Delivery**
**Purpose of this file:** This is the evidence base. Every claim in `idea.md` and `PLAN.md` traces back to a numbered fact here. Nothing here is invented; where a number could not be verified against a primary source, it is explicitly flagged.

---

## Table of Contents

- [0. How to read this document](#0-how-to-read-this-document)
- [1. What the hackathon is actually asking](#1-what-the-hackathon-is-actually-asking)
- [PART A — THE INDIAN REALITY](#part-a--the-indian-reality)
  - [A1. What CAG audits actually found](#a1-what-cag-audits-actually-found)
  - [A2. MGNREGA social audits: detection vs recovery](#a2-mgnrega-social-audits-detection-vs-recovery)
  - [A3. AuditOnline — the most damning screen in Indian GovTech](#a3-auditonline--the-most-damning-screen-in-indian-govtech)
  - [A4. NMMS — the attendance app that gets fudged](#a4-nmms--the-attendance-app-that-gets-fudged)
  - [A5. Wage delays — proof that MIS forensics works at scale](#a5-wage-delays--proof-that-mis-forensics-works-at-scale)
  - [A6. Bribery rates](#a6-bribery-rates)
  - [A7. Public procurement](#a7-public-procurement)
  - [A8. PDS leakage and DBT](#a8-pds-leakage-and-dbt)
  - [A9. Grievance redressal — CPGRAMS](#a9-grievance-redressal--cpgrams)
  - [A10. RTI — the appeal that takes 29 years](#a10-rti--the-appeal-that-takes-29-years)
  - [A11. What data a prototype can ACTUALLY pull](#a11-what-data-a-prototype-can-actually-pull)
  - [A12. The last-mile problem](#a12-the-last-mile-problem)
- [PART B — THE ACADEMIC STATE OF THE ART](#part-b--the-academic-state-of-the-art)
  - [B1. Procurement fraud & collusion detection](#b1-procurement-fraud--collusion-detection)
  - [B2. Graph anomaly detection / GNN fraud](#b2-graph-anomaly-detection--gnn-fraud)
  - [B3. GraphRAG & knowledge graphs + LLMs](#b3-graphrag--knowledge-graphs--llms)
  - [B4. Indic NLP and speech](#b4-indic-nlp-and-speech)
  - [B5. Document AI / OCR on messy government paper](#b5-document-ai--ocr-on-messy-government-paper)
  - [B6. Entity resolution](#b6-entity-resolution)
  - [B7. LLM agents over structured data — reliability](#b7-llm-agents-over-structured-data--reliability)
  - [B8. Satellite & computer vision for asset verification](#b8-satellite--computer-vision-for-asset-verification)
  - [B9. On-device / edge AI](#b9-on-device--edge-ai)
  - [B10. Crowdsourcing integrity & image forensics](#b10-crowdsourcing-integrity--image-forensics)
  - [B11. Privacy](#b11-privacy)
- [PART C — FEASIBLE TODAY vs STILL RESEARCH](#part-c--feasible-today-vs-still-research)
- [PART D — THE GAP ANALYSIS (where the idea comes from)](#part-d--the-gap-analysis-where-the-idea-comes-from)
- [PART E — RELIABILITY NOTES](#part-e--reliability-notes)

---

## 0. How to read this document

Three conventions are used throughout:

| Marker | Meaning |
|---|---|
| ✅ | I opened the primary source and read the number directly. |
| 📰 | Verified via reputable journalism reporting a primary document (a CAG report, a study) that I did not open myself. Safe to cite *with attribution to the reporting outlet*. |
| ⚠️ | **NOT verified.** Do not put this on a slide without opening the source first. |

**A methodological caution that shapes the entire design.** Three separate 2026 papers independently show that published numbers in exactly the areas this project cares about are *inflated*:

- Leakage-safe evaluation protocols "reduce previously inflated accuracy estimates by a notable margin" in procurement ML — **ERP-RiskBench** (arXiv:2603.06671)
- A realistic anti-money-laundering benchmark "yields substantially lower detection performance than widely used benchmarks" — **TransXion** (arXiv:2604.17420)
- The geospatial foundation-model literature contains **46 documented cross-paper contradictions of ≥10 points on identical model/benchmark/protocol setups**, and **39% of GFM papers release no weights** — (arXiv:2605.12678)

**Consequence:** wherever a number appears twice in the literature — an optimistic in-distribution one and a pessimistic out-of-distribution one — this document quotes the pessimistic one. The design in `idea.md` is built to survive the pessimistic number. That is a deliberate scoring strategy for the *Feasibility & Implementation Readiness* rubric line.

---

## 1. What the hackathon is actually asking

From `about.txt`, the framing question is:

> *"How can India drive inclusive growth and equitable access to opportunities by leveraging innovation, technology, and community-driven solutions that empower underserved populations, improve financial inclusion, strengthen public service delivery, and enhance quality of life?"*

And the specific sub-theme selected:

> **GovTech & Public Service Delivery** — *"How can technology improve the efficiency, transparency, accessibility, and citizen-centric delivery of government services and public welfare programs?"*

### The scoring rubric (100 marks)

| # | Criterion | What it really tests |
|---|---|---|
| 1 | Problem-Solution Fit | Is the problem *real and evidenced*, and does each component of the solution map to a specific failure? |
| 2 | Innovation & Uniqueness | Has this been done before? Can you prove it hasn't? |
| 3 | Feasibility & Implementation Readiness | Can it be built? Is there a prototype? Do you know your own limits? |
| 4 | Scalability & Sustainability | Does it work for 2.5 lakh panchayats, not 1 village? Who pays for it in year 3? |
| 5 | Impact Potential | Measurable, in rupees and in people. |
| 6 | Alignment with National Priorities | Viksit Bharat 2047, Digital India, DBT, Bhashini, RTI Act, DPDP Act. |
| 7 | Presentation & Communication | The narrative. |

### Hard eligibility constraints

- Indian nationals, 18+ as on 30 May 2026
- Individual or team of 2–4
- **Must include a prototype, pilot, proof of concept, or demonstrable model** — this is not an ideas-only competition
- Solutions governed under **MIT Open Source License**
- Final submission is final; no resubmission
- Prize pool ₹2,00,000; Jul 01 – Oct 07, 2026; online

### Required submission sections

1. Problem Statement Identification
2. Solution Overview, Innovation & Differentiation
3. Technology or Implementation Framework
4. Prototype / Pilot Details
5. Scalability & Sustainability Plan
6. Expected Social & Economic Impact
7. Team Information
8. Supporting Documents

> **Design implication:** the MIT-license requirement plus the prototype requirement means the winning entry must be built on **openly licensed models and openly accessible data**. This rules out any design that depends on proprietary satellite imagery, gated APIs, or closed model weights as a *core* dependency. Everything in `idea.md` is buildable on free, public, permissively-licensed inputs. That is not an accident.

---

# PART A — THE INDIAN REALITY

## A1. What CAG audits actually found

The Comptroller and Auditor General is India's constitutional auditor. Its reports are the highest-trust evidence available on scheme leakage. Here is what recent ones say.

### A1.1 Jal Jeevan Mission, Maharashtra (tabled July 2026) 📰

| Finding | Number |
|---|---|
| Water supply schemes taken up 2019–2024 | 51,560 |
| **Completed** | **12,703 (24.64%)** |
| **Incomplete** | **38,857 (75.30%)** |
| Original estimate | ₹13,668 crore |
| Allocation | ₹27,559.26 crore |
| **Actual spend by March 2024** | **₹26,410.51 crore** |
| **Households omitted from District Action Plans entirely** | **1,08,000** |
| Schemes needing cost revision | 13,835 (27%), inflating cost by ₹9,608.87 crore |
| Mandatory baseline survey | **Never conducted** |

📰 *Source: IANS wire report on CAG Performance Audit of Jal Jeevan Mission, Govt of Maharashtra, 2026 — https://www.lokmattimes.com/national/planning-failures-double-mahas-jal-jeevan-mission-cost-to-rs-26410-cr-cag/*
✅ *Primary index: https://cag.gov.in/en/audit-report/details/125424*

**Read that again:** costs doubled while three-quarters of the schemes were never finished, and the baseline survey that was supposed to tell them where the water was never happened.

### A1.2 MGNREGA, Karnataka (performance audit FY2019-20 → FY2023-24, tabled 24 March 2026) 📰

| Finding | Number |
|---|---|
| Rural households given the full 100 days over five years | **5%** |
| Job cards issued (2023-24) | 79.09 lakh |
| Households that sought work | 32.41 lakh |
| Households that got work | 29.96 lakh |
| **Households that got all 100 days** | **0.43 lakh (43,000)** |
| **Average share of "active" workers** | **~40%** |
| **⇒ Registered workers who never worked** | **~60%** |
| Works flagged by social audits for misappropriation, Karnataka alone | ⚠️ **figure withdrawn** — the previously-listed ₹5,275 crore could not be corroborated against any primary source; state Social Audit Directorate totals reported elsewhere are far smaller. Do not cite a Karnataka-specific total without the CAG/SAD source |

CAG's own words on the inactive share: *"the existence of ghost workers, failure of gram panchayats to undertake annual updating exercise of job cards, poor awareness levels of entitlements."*

And on the payments: *"fraudulent transactions such as payment for houses already completed, payment to ineligible beneficiaries and payments without undertaking construction."*

📰 *Source: Deccan Herald — "60% of registered MGNREGA workers not active in Karnataka" (https://www.deccanherald.com/india/karnataka/60-of-registered-mgnrega-workers-not-active-in-karnataka-3566168).* ⚠️ *The precise active/inactive share varies across reporting (≈40% active / ≈60% inactive is used here). Confirm against the primary CAG report — MGNREGS, Karnataka, year ended March 2024 (cag.gov.in) — before citing an exact percentage in the formal submission.*

### A1.3 The forensic detail — this is the single most important passage in this document 📰

From the same Karnataka CAG report, housing-works component:

| Finding | Number |
|---|---|
| Gram panchayats examined | 39 |
| Housing works | 2,560 |
| **Projects scrutinised** | **847, worth ₹1.91 crore** |
| **Found misappropriated** | **₹1.19 crore** |
| **Irregularity rate in sampled works** | **56% to 99%** |
| Payments for foundation/lintel/roofing on **houses already completed** | **462 instances** |
| Payments exceeding the 90 man-day limit | 117 cases |
| Payments to landless/ineligible beneficiaries | 8 cases |
| **Works where NO work was executed at all, yet payment was processed** | **12 cases** |

And then the two details that define this entire project:

> **1. "Identical photographs were uploaded across different construction stages to fake progress."**
>
> **2. "Auditors used satellite imagery and Google Earth historical data; in several cases no physical structure existed at the claimed location."**

Two specific cases:
- **Kalaburagi (Kamalapur taluk), solid-waste shed:** >₹18 lakh spent, work incomplete; muster rolls, bills and **geo-tagged images tampered with**; materials shown as purchased *after* project completion.
- **Koppal (Yelburga taluk), check dam:** the work was **split into two smaller works to bypass tendering**; supplier invoices missing; **>₹10 lakh paid without verification.**

And the kicker:

> **CAG explicitly noted "social audits failed to detect any discrepancies" in these cases.**

📰 *Source: Organiser, 7 April 2026, reporting the CAG report tabled in the Karnataka legislature — https://organiser.org/2026/04/07/347536/bharat/karnataka-massive-misappropriation-under-mgnrega-exposed-in-the-state-cag-flags-systemic-failures/*

> ⚠️ **Editorial note on this source.** *Organiser* is an RSS-affiliated publication. The underlying document is a CAG report tabled in a state legislature, and the headline findings (ghost workers, fraudulent payments, record fabrication) are independently corroborated by Deccan Herald above. **Treat the granular sub-figures — 462, 12, 847, ₹1.19 crore — as requiring confirmation against the CAG PDF before appearing in a formal submission.** For the hackathon deck, cite the Deccan Herald headline findings and describe the forensic pattern qualitatively.

**Why this matters more than anything else here:**

CAG caught this fraud using **four techniques, all of which are trivially automatable and none of which are automated today**:

| What CAG did by hand | What it is, computationally |
|---|---|
| Noticed the same photo across different "stages" | **Perceptual hashing.** ~40 lines of Python. Runs on millions of images in hours. |
| Opened Google Earth to check if a structure existed | **Bi-temporal satellite change detection.** Free Sentinel-2, published models. |
| Spotted a check dam split in two to dodge the tender threshold | **Threshold-splitting detection.** A `GROUP BY` and a histogram. |
| Found materials "purchased after completion" | **Temporal consistency check.** A date comparison. |

An audit that took months of expert human effort across a 39-panchayat *sample* is, in every one of its four detection mechanisms, a batch job. **That is the entire thesis of this project.**

### A1.4 PM-POSHAN / Mid-Day Meal, Odisha (year ending March 2023) 📰

| Finding | Number |
|---|---|
| Schools checked | 642 across 5 districts |
| Schools showing more meals served than students present | **42** |
| **Phantom meals** | **82,270 primary + 1,36,546 upper-primary ≈ 2.19 lakh** |
| Inflated claims | ₹9.12 lakh rice + ₹14.33 lakh cooking cost ≈ ₹23.45 lakh |
| Food security allowance for 179 students routed to **headmasters' personal accounts** | ₹1,19,562 |
| **Schools with NO infrastructure at all that still claimed expenditure** | **2** (Denguni and Ambadhuni, Muniguda) — **₹3.05 lakh and 55.94 quintals of rice over 5 years** |

📰 *Source: The New Indian Express, 2 April 2026 — https://www.newindianexpress.com/states/odisha/2026/Apr/02/odisha-schools-cooked-up-more-mid-day-meals-than-students-cag*
✅ *Primary: https://cag.gov.in/en/audit-report/details/125073 (page returned an XML parse error on fetch; PDF linked from the cag.gov.in index)*

### A1.5 Gaps I could not fill

- **PMAY-G, PMGSY roads, Swachh Bharat:** no recent quotable *national* CAG figures found in this pass. State reports exist at `https://cag.gov.in/en/audit-report` but findings are locked in untagged PDFs. ⚠️ **Do not cite numbers for these three without opening the specific report.**
- ⚠️ Maharashtra "92 lakh bogus Ladki Bahin beneficiaries after verification" — politically-sourced secondary reporting, unverified.

---

## A2. MGNREGA social audits: detection vs recovery

This is the strongest evidence base available, because **the government itself publishes both the fraud detected and the amount recovered.**

### A2.1 The national picture 📰

| Financial year | Misappropriation detected |
|---|---|
| 2020-21 | ₹115.02 crore |
| 2021-22 | ₹215.72 crore |
| 2022-23 | ₹160.01 crore |
| 2023-24 | ₹169.76 crore |
| 2024-25 | ₹228.57 crore |
| 2025-26 (to 23 Sep 2025) | ₹110.89 crore |
| **Cumulative** | **> ₹1,000 crore** |
| **Total recovered** | **₹122.66 crore — under 13%** |
| **⇒ Untraced** | **≈ ₹878 crore** |

Further detail:
- FY2020-21 → FY2024-25 alone: **₹889.19 crore** detected, with audit coverage ranging **52.64%–79.01%** of 2,69,243 panchayats.
- FY2025-26 (to 23 Sep 2025): audits covered only **1,03,885 panchayats = 38.58%**, and *still* found **61,347 separate cases**.
- Scheme scale: **~12 crore active rural workers** (MGNREGA MIS; the exact figure drifts by date across roughly 11.9–14.3 crore — cite with a date if used).
- **Tamil Nadu example:** 6,470 of 12,525 panchayats audited (51%); **₹26.57 crore across 21,169 cases**; **only ₹1.33 crore traced.**

📰 *Source: DT Next, 24 September 2025 — https://www.dtnext.in/news/tamilnadu/mgnregs-rs-1000-cr-siphoned-off-in-6-yrs-recovery-below-10-pc-847489*

✅ **Primary source (live, government-run):** *R 9.2.6 Financial Misappropriation Recovery Report*, Social Audit Findings, NREGASoft —
`https://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SAU_FMRecoveryReport.aspx`

> ⚠️ **Critical engineering constraint discovered during research.** This URL **rejects direct deep-links with the error "URL Tampered"**. NIC enforces referrer/session validation. It must be reached by *navigating* from `https://mnregaweb4.nic.in/netnrega/MISreport4.aspx`. Any scraper must be session-aware. Budget real engineering time for this. See `PLAN.md` §4.2.

📰 Corroborating: **₹169.75 crore misappropriated nationally in 2023-24, only ₹20.93 crore recovered** — Hindustan Times, 2025 (⚠️ page redirected to an ad-server on fetch; figure from search-index snippet, confirm before citing). Maharashtra 2024-25: audits in **6,665 of 28,292 panchayats revealed 5,176 cases**.

### A2.2 The framing that wins the room

> Detection is **supply-constrained, not demand-constrained.** In 2025-26, auditing only **38.58%** of panchayats surfaced **61,347 cases**. An official quoted by DT Next estimated that at 75% coverage, detected misappropriation would **cross ₹250 crore in a single year.**
>
> India is not failing to find corruption because corruption is hard to find. It is failing because there are not enough auditors, and the ones there are do the work by hand.

---

## A3. AuditOnline — the most damning screen in Indian GovTech

✅ **Verified live, 29 July 2026** — `https://auditonline.gov.in/` (Ministry of Panchayati Raj). National counters, FY 2025-26:

| Metric | Value |
|---|---|
| Enlisted auditees | **262,202** (635 Zilla Parishads, 6,165 Block Panchayats, **255,402 Gram Panchayats**) |
| Enlisted auditors | 12,695 |
| Year books closed | 247,075 |
| **Audit plans prepared** | **72,186 — 27.5% of auditees** |
| **Observations recorded** | **62,745** |
| **Audit reports generated** | **5,657 — 2.2% of auditees** |
| **Settlement reports generated** | **0** |
| **Action Taken Reports** | **0** |

> **The government built the platform. It onboarded a quarter of a million panchayats. It recorded 62,745 audit observations. And it closed zero of them.**
>
> The last mile of accountability — *finding → responsible officer → recovery order → amount recovered → case closed* — **is not digitised at all.**

This single table is the strongest justification for Layer 5 of the proposed system (the Accountability Clock). It is not a hypothesis about a gap. It is a live government dashboard reporting zero.

---

## A4. NMMS — the attendance app that gets fudged

The National Mobile Monitoring System mandates twice-daily geo-tagged photo attendance at every NREGA worksite. It generates **millions of geo-tagged photographs**. Nobody analyses them.

- 📰 **The Ministry of Rural Development itself directed states to improve NMMS monitoring after finding the system was being fudged.** — Times of India, 19 July 2025 (⚠️ fetch blocked by ad-redirect; headline/date from search index)
- 📰 Government's own review found the digital attendance system **"riddled with holes"** — The Hindu, 2025 (⚠️ article ID no longer resolves)
- ✅ Academic assessment: *"MGNREGA's Attendance App"*, **Economic & Political Weekly**, Vol 59 Issue 48, 30 Nov 2024 — https://www.epw.in/journal/2024/48/commentary/mgnregas-attendance-app.html
- ✅ **NREGA Sangharsh Morcha formally demanded rollback of NMMS**, August 2025 — https://www.counterview.net/2025/08/nrega-sangharsh-morcha-demands-rollback.html
- 📰 Documented failure mode: a Telangana worker in Mahabubabad **could not mark attendance after shaving his head** until he borrowed a hair cover — face-match rejected him.

> **The design lesson.** NMMS made attendance *harder for honest workers* and *no harder for dishonest supervisors*, because nobody runs forensics on the resulting images. A shaved head blocks a real worker; a recycled photograph passes. **Surveillance was added without verification.** The proposed system inverts this: it runs forensics on the images the state already collects, and it never adds a new burden on the worker.

---

## A5. Wage delays — proof that MIS forensics works at scale

✅ **LibTech India / Azim Premji University.** Analysis of **31.36 million transactions across 10 states, FY 2021-22, crawled directly from the MGNREGA MIS.**

| Finding | Number |
|---|---|
| Wage payments delayed beyond the mandated 7 days | **63%** |
| Delayed beyond 15 days | **42%** |

✅ *https://libtech.in/wp-content/uploads/2023/08/MGNREGA_TechLab_WageDelays_CasteABPS_Aug29_2023.pdf*
✅ *Peer-reviewed: https://link.springer.com/article/10.1007/s41027-024-00539-9*
✅ *National tracker 2019-24: https://libtech.in/wp-content/uploads/2024/07/India-MGNREGA-Report-2019-24-Eng.pdf*

> **Why this citation is load-bearing.** It is the existence proof. A small civil-society team crawled 31 million government transactions and published national findings. **The data is reachable. The scale is tractable. It has already been done once.** Any judge asking "can you really get this data?" is answered by LibTech.

---

## A6. Bribery rates

### A6.1 Transparency International — Global Corruption Barometer Asia 2020 ✅

| Finding | Number |
|---|---|
| **India's bribery rate — highest in Asia** | **39%** paid a bribe for a public service in the last 12 months |
| **Used personal connections** to access public services — also highest in Asia | **46%** |
| Say government corruption is a big problem | **89%** |
| Of those who paid a bribe, share who were *asked* to pay | ≈50% |
| Asia-wide, people who paid a bribe | ~1 in 5 ≈ **836 million people** |

✅ *https://files.transparencycdn.org/images/GCB_Asia_2020_Report_Web_final.pdf*

### A6.2 CMS India Corruption Study 2018 ✅ (headline) / ⚠️ (breakdown)

| Finding | Number |
|---|---|
| Households across 13 states feeling corruption increased or stayed the same | **75%** |
| Households that paid a bribe in the previous year | **27%** |
| Households **denied service outright** for inability to pay a bribe (PDS and Police) | **~2%** |

✅ *https://www.cmsindia.org/sites/default/files/2019-05/CMS_ICS_2018_Report.pdf*

> ⚠️ **The service-wise breakdown you would want — land records vs police vs municipal vs PDS vs electricity — is inside that PDF and could not be extracted.** The CMS study historically ranks police and land/registration highest, but no percentages are stated here because none were read. Download the PDF before using service-level numbers.

---

## A7. Public procurement

### A7.1 Scale ✅ (live, 29 July 2026)

**GeM (Government e-Marketplace)** — `https://gem.gov.in/`
- 10,578 product categories, 350 service categories
- **Cumulative order value: ₹19,83,628 crore (≈ ₹19.8 lakh crore)**

**CPPP / GeM-CPPP** — `https://eprocure.gov.in/cppp/`
- **97,884 active tenders**; 8,761 opening today; 9,429 closing today; 38,514 GeM bids
- **Publishes Bid Awards publicly:** `https://eprocure.gov.in/cppp/resultoftendersnew`

### A7.2 CVC (Central Vigilance Commission)

- ✅ CVC publishes annual reports for **1986–2024 as PDFs only** — no structured data, no API, no CSV. `https://www.cvc.gov.in/annualreport`
- ⚠️ From CVC AR 2024 (secondary): 200 cases pending for prosecution sanction under the Prevention of Corruption Act 1988 across 46 organisations; 60 departmental action cases pending against CBI personnel. *Verify against the PDF.*
- ⚠️ >7,000 CBI corruption cases pending in courts, 379 pending more than 20 years. *Low-quality secondary source.*
- Machine-readable derivatives exist commercially: `https://dataful.in/collections/658/` — i.e. **a private company has to re-key the PDFs.**

### A7.3 The gap that is a gift ✅

> **There is no published national statistic for the single-bid tender rate in India.**
>
> I searched for it. It does not exist as an official figure. CVC has *guidelines* on single-bid tenders, but neither CVC, nor CPPP, nor GeM publishes an aggregate "% of tenders that received only one bid."

This matters enormously, because **single-bidder rate is the headline red-flag indicator** used by the World Bank, the EU's DIGIWHIST/Opentender project, and Fazekas's Government Transparency Institute. It is the first number any procurement-corruption analyst computes.

CPPP publishes bid-award results publicly. Computing:
- **single-bid rate**
- **repeat-winner concentration (HHI)**
- **award-value-vs-estimate variance**
- **tender advertisement-period shortening**

…by procuring entity is a *tractable analysis that nobody in India publishes*. A working prototype that produces India's first single-bid-rate table is, by itself, a novel public good.

### A7.4 Bid rigging / CCI

- CCI has an established bid-rigging enforcement record — *Lakshmikumaran & Sridharan, 8 July 2022* — https://www.lkslaw.com/insights/articles/bid-rigging-in-public-procurement-an-indian-perspective
- ⚠️ HP fined ₹1.42 billion (≈₹142 crore) for manipulating Indian government tenders for cartridges, toners, PCs (Reuters via Yahoo Finance, July 2026). *Verify the CCI order before citing.*
- CCI annual reports: `https://cci.gov.in/annual-report`

---

## A8. PDS leakage and DBT

### A8.1 Leakage over two decades ✅

| Study | 2004-05 | 2011-12 | 2022-23 | 2023-24 |
|---|---|---|---|---|
| Drèze & Khera (2015) | 54% | 41.7% | — | — |
| Bhattacharya et al. (2017) | 58.6% | 43.1% | — | — |
| Gulati & Saini (2015) | — | 46.7% | — | — |
| Khera (2024) | — | — | 22.1% | — |
| Das et al. (ICRIER, 2024) | — | — | 28% | — |
| **Puri & Pingali (2025)** | — | — | **24.1%** | **8.8%** |

✅ *Pingali & Puri, Ideas for India / Tata-Cornell Institute, 11 Aug 2025 — https://www.ideasforindia.in/topics/poverty-inequality/declining-pds-leakages-a-look-at-the-numbers*

> **The caveat the authors themselves raise, and which you must repeat if you cite this:** the 2023-24 estimates are **negative for five states — Assam, Bihar, Jharkhand, Rajasthan, Uttar Pradesh** — which is arithmetically impossible. It indicates the underlying data (RGI population projections, the delayed 2021 Census, HCES consumption over-reporting) is unreliable. **The authors conclude actual leakage is "likely in the range of 10–20%."**

⚠️ ICRIER estimate: **28% of grains do not reach beneficiaries — about 20 million tonnes, worth ₹69,108 crore annually.** *PDF fetch failed; figure taken from Economic Times, 18 Nov 2024. Verify.*

### A8.2 DBT Bharat — the government's own savings claims ✅ (up to March 2025)

**Headline: estimated gains ₹5,14,201.92 crore.**

| Scheme | Estimated gain (₹ crore) | Government's stated basis |
|---|---|---|
| **PDS** | **3,12,977.81** | **Deletion of 6.36 crore duplicate/fake/non-existent ration cards** |
| **MGNREGS** | **74,888.19** | **Deletion of 1.32 crore fake and duplicate job cards (FY2022-25)** |
| **PAHAL (LPG)** | **74,031.34** | **Elimination of 4.09 crore duplicate/fake/inactive LPG connections** |
| PM-KISAN | 22,106.14 | 2.1174 crore ineligible beneficiaries deleted |
| Fertilizer | 18,699.89 | 158.06 lakh MT reduction in sales to retailers |
| Minority scholarships | 2,296.81 | 37.77 lakh duplicate/fake deleted |
| PMEGP | 2,043.36 | 52,584 duplicate/ineligible deleted |
| Anganwadi Services | 1,523.75 | 98.8 lakh duplicate/fake deleted |
| SJE scholarships | 1,054.65 | 12.28 lakh duplicate/fake deleted |
| NSAP | 1,029.31 | 6.99 lakh ineligible/duplicate deleted |
| PMAY-U | 301.78 | 20,119 duplicate/ineligible deleted |
| PMAY-G | 21.04 | 8,047 ineligible/duplicate deleted |
| **Total** | **5,14,201.92** | |

✅ *https://dbtbharat.gov.in/static-page-content/spagecont?id=18*
✅ Platform scale: cumulative DBT **₹52,59,762 crore**; 318 schemes; 56 ministries; FY2026-27 to date ₹1,42,378 crore across 168 crore transactions — `https://dbtbharat.gov.in/`

### A8.3 The central tension — this is the pitch

> The government says it deleted **1.32 crore fake MGNREGA job cards** in three years.
>
> CAG says **about 60% of registered workers in Karnataka were not active** and calls them ghost workers.
>
> Social audits detected **₹1,000+ crore** of misappropriation and recovered **under 13%**.
>
> **Deduplication is not accountability.** Deleting a fake job card stops *future* theft. It does not recover the money already taken, identify who took it, or verify whether the asset that was paid for exists. India has built world-class *plumbing* (Aadhaar, DBT, PFMS, UPI) and almost no *forensics*.

### A8.4 Aadhaar-based exclusion — the counter-argument you must pre-empt

Key literature identified (⚠️ **percentages not retrieved — do not cite numbers without opening these**):

- Drèze, Khalid, Khera & Somanchi, **"Aadhaar and Food Security in Jharkhand: Pain without Gain?"**, *EPW* 2017 — https://www.jstor.org/stable/45132599
- Muralidharan, Niehaus & Sukhtankar — large-scale experiment across **15 million beneficiaries** on stringent Aadhaar-based biometric authentication in PDS — https://www.ideasforindia.in/topics/poverty-inequality/balancing-corruption-and-exclusion-incorporating-aadhaar-into-pds
- Khera & Somanchi rejoinder — https://www.ideasforindia.in/topics/poverty-inequality/balancing-corruption-and-exclusion-a-rejoinder

> **Why this matters for the design.** Every anti-fraud intervention in Indian welfare has produced **exclusion errors** — real beneficiaries locked out. A judge who knows this literature will ask: *"how is your system not another Aadhaar-seeding disaster?"*
>
> The answer must be architectural, not rhetorical: **the proposed system never sits between a citizen and their entitlement.** It has no authority to deny a payment, block a job card, or gate a ration. It is a *read-only forensic and grievance layer* that runs after the money has moved. It can only ever *add* a case file, never subtract an entitlement. **A false positive costs an official an explanation; it never costs a citizen their rice.** That asymmetry must be stated explicitly in the deck.

### A8.5 One Nation One Ration Card (IMPDS) ✅

**Live, public, and exportable.** `https://impds.nic.in/` publishes a **state-to-state portability matrix** with a one-click *"Export table as Excel."*

Single-day snapshot: **134,906 portability transactions, 129,563 ration cards, 591,612 beneficiaries, 2,295,029.73 kg wheat, 677,489.70 kg rice** across 17 states, with full origin × destination breakdown (Delhi→Bihar 284,524; Maharashtra→UP 58,520).

---

## A9. Grievance redressal — CPGRAMS

### A9.1 National aggregates ✅ (Parliament answer — primary source)

For **1 Nov 2022 – 26 May 2025**, Central Government Ministries/Departments/Organisations:

| Brought forward | Received | Closed | Pending (26.5.2025) | Avg. disposal |
|---|---|---|---|---|
| 75,790 | **42,62,459** | 42,73,289 | **64,960** | **16 days** |

✅ *PIB Release ID 2152955, 6 Aug 2025 — https://pib.gov.in/PressReleaseIframePage.aspx?PRID=2152955*

Also from the same answer — **all of which is infrastructure the proposed system can reuse rather than rebuild**:
- Resolution timeline **reduced from 30 to 21 days** (Comprehensive Guidelines, 23 Aug 2024)
- CPGRAMS available in **all 22 scheduled languages**
- **Multilingual Feedback Call Centre**; poor ratings **auto-trigger an appeal option**; departments can access **audio transcripts**
- **Integrated with Common Service Centres (CSCs)** for rural outreach
- >1 lakh grievances redressed per month for three years running
- 2025 update: avg disposal **15 days** (from 22 in 2022); **>10.7 lakh citizen feedbacks, 66% via the Feedback Call Centre**; **IGMS 2.0 with AI/ML analytics and a Bhashini-powered multilingual voice chatbot deployed**; 223 senior review meetings identified **52 systemic policy issues** ✅ *PIB 2177187, 10 Oct 2025*

### A9.2 The live public dashboard ✅ (1 Jan – 28 Jul 2026)

Fully public, department-wise HTML table — ideal prototype input. `https://pgportal.gov.in/darpgdashboard`

**Highest volumes:**

| Department | Received | Disposal % | Pending |
|---|---|---|---|
| Labour and Employment | 1,89,445 | 90.04% | 17,819 |
| Financial Services (Banking) | 1,74,041 | 96.92% | 5,352 |
| Home Affairs | 57,715 | 96.47% | 2,016 |
| Railways | 56,334 | 90.41% | 4,759 |
| Telecommunications | 55,558 | 96.09% | 2,169 |
| Petroleum and Natural Gas | 53,870 | **77.53%** | **10,030** |

**Worst disposal rates:**

| Department | Disposal % |
|---|---|
| **Petroleum and Natural Gas** | **77.53%** |
| **Rural Development** | **81.13%** (3,372 pending) |
| Higher Education | 85.94% |
| **Panchayati Raj** | **87.11%** |
| Defence Finance | 87.93% |
| Ex-Servicemen Welfare | 88.02% |
| Economic Affairs | 89.01% |

> **Note the pattern: the departments running rural welfare schemes are the worst performers on citizen grievances.** Rural Development 81.13%, Panchayati Raj 87.11% — against a Home Affairs 96.47% and Banking 96.92%. The people with the least ability to escalate get the worst service.

The dashboard also tracks grievances pending **>30 days** and **>60 days** — e.g. Petroleum & Natural Gas has **2,068** beyond 30 days; Panchayati Raj has **411 beyond 30 days and 46 beyond 60 days.**

⚠️ DARPG does **not** publish a headline reopen rate or citizen satisfaction score. **Do not cite a satisfaction percentage.**

### A9.3 State-level ✅

- **UP Jansunwai–Samadhan (IGRS)** — `https://jansunwai.up.nic.in/` — live portal, separate citizen and officer Android apps, plus linked **Anti-Corruption Portal** (`acp-cm.up.gov.in`), **Anti Bhu-Mafia Portal** (`abmp.up.gov.in`), **CM Dashboard** (`cmis.up.gov.in`).
- The portal explicitly routes non-UP grievances to CPGRAMS — **there is federation, but no unified national grievance dataset.**

---

## A10. RTI — the appeal that takes 29 years

From the **Report Card on the Performance of Information Commissions in India, 2024–25** (Satark Nagrik Sangathan, October 2025, marking 20 years of the RTI Act, compiled from information obtained *under the RTI Act itself*):

| Finding | Number |
|---|---|
| **Appeals and complaints pending nationally** | **> 4.13 lakh** |
| **Information commissions defunct for part of the period** | **6 of 29** |
| **Time for Telangana SIC to dispose one new appeal filed 1 July 2025** | **> 29 years** |

📰 *Key findings: https://www.snsindia.org/wp-content/uploads/2025/10/Report-Card-Key-findings-2025.pdf*
📰 *Corroborating: Times of India, Oct 2025 — https://timesofindia.indiatimes.com/india/over-4-lakh-cases-pending-in-information-commissions-across-india/articleshow/124431507.cms*

> ⚠️ The SNS PDFs returned "failed to extract meaningful content" on fetch and Clarion India returned HTTP 403. The three figures come from search-index snippets plus TOI and Shankar IAS summaries, which are mutually consistent. **Open the SNS PDFs before putting these on a slide.**

✅ **And note the meta-point:** *there is no machine-readable government dataset of information-commission case disposal.* SNS has to **file RTIs to find out how RTIs are being handled.** That is itself a transparency failure worth citing.

---

## A11. What data a prototype can ACTUALLY pull

**This is the most important section for feasibility scoring.** Each of these was tested live on 29 July 2026.

### ✅ Genuinely public + machine-readable

| Source | URL | What you get | Access |
|---|---|---|---|
| **API Setu** | `https://apisetu.gov.in/` · `https://directory.apisetu.gov.in/` | **8,900+ published APIs, 2,900+ publishers**; 182 central-govt orgs, 2,400 state-govt orgs | REST + OpenAPI specs |
| **Local Government Directory (LGD)** ⭐ | `https://lgdirectory.gov.in/` · API `https://dev.napix.gov.in/nic/lgd/` | **36 States/UTs, 784 districts, 7,092 sub-districts, 7,323 blocks, 677,042 villages (657,769 inhabited), 262,726 rural local bodies incl. 255,297 gram panchayats.** Plus exception reports | **Bulk "Download Directory" + NAPIX API** |
| **IMPDS / ONORC** | `https://impds.nic.in/` | Daily state×state ration portability matrix | **"Export table as Excel"** |
| **CPGRAMS dashboard** | `https://pgportal.gov.in/darpgdashboard` | Dept-wise received/disposed/%/pending/>30d/>60d, date-range selectable | Public HTML, scrapable, no login |
| **CPPP (GeM-CPPP)** | `https://eprocure.gov.in/cppp/` | 97,884 active tenders; **Bid Awards** at `/resultoftendersnew`; corrigenda | Public HTML + downloads |
| **AuditOnline** | `https://auditonline.gov.in/` | Year-book closure, audit plans, observations, reports, settlements, ATRs — by ZP/BP/GP/year | Citizen Section; **PDF + Excel download** |
| **eGramSwaraj** | `https://egramswaraj.gov.in/` | Panchayat profiles, GPDP plans, accounting/financial progress, PFMS dashboard, bank-wise pending payments | Public dashboards + **published API spec** `eGramSwaraj_api_integration_v3.0.pdf` |
| **data.gov.in** | `https://data.gov.in/` | OGD platform under **Government Open Data License – India (GODL)** | RSS `https://data.gov.in/backend/dms/v1/rss.xml` (⚠️ old `/ogpl_apis` path now 404s) |
| **DBT Bharat** | `https://dbtbharat.gov.in/` | Scheme-wise gains, transaction totals, state ranking | HTML, scrapable |

> ⭐ **LGD is the single most important item in this table.** LGD codes were **mandated as the standard location code across all e-Government applications by the Cabinet Secretariat on 4 November 2016.** Every portal above uses them. **They are the join key that makes a unified graph possible.** Without LGD there is no project; with it, joining eleven portals is a merge on an integer.

### ⚠️ Public but awkward — needs engineering

| Source | Problem |
|---|---|
| **NREGASoft / MGNREGA MIS** (`nrega.nic.in`, `mnregaweb4.nic.in`) | **Richest data in Indian GovTech** — job cards, muster rolls, works, payments, **social audit findings, the Financial Misappropriation Recovery Report.** But deep-links are rejected with **"URL Tampered"** (referrer/session validation), and reports are **ASP.NET postback forms**. You must crawl by walking navigation from `MISreport4.aspx`. **Proof it's doable: LibTech crawled 31.36M transactions across 10 states this way.** |
| **PFMS** (`pfms.nic.in`) | **Main portal login-gated.** Public dashboard `https://pfmsdashboard.gov.in/` returned no extractable content. **Transaction-level scheme spending is NOT openly published.** The system that moves the money does not expose the ledger. |
| **CAG** (`cag.gov.in`) | **PDFs only.** No structured audit-observation database, no API, no tagging of paragraphs by scheme/district/amount. One report page returned an XML parse error. |
| **CVC** (`cvc.gov.in`) | **PDFs only**, 1986–2024. No structured complaint data. |
| **GeM** (`gem.gov.in`) | Headline counters public; bid list at `https://bidplus.gem.gov.in/all-bids`. Granular award-level data not offered as bulk download. |

### ❌ Not available at all

- **PFMS transaction-level scheme spending**
- **A national single-bid tender rate** — nobody publishes it
- **CPGRAMS grievance text corpus or API** — dashboard only
- **Information commission case-level data** — obtained only by filing RTIs
- **ULB / Panchayat asset registers** — **no national machine-readable asset register exists.** eGramSwaraj holds works data, NREGASoft holds geo-tagged asset photos, but there is no consolidated, queryable public asset inventory. **This is a genuine void.**

---

## A12. The last-mile problem

### A12.1 The headline numbers look great. The disaggregation does not. ✅

From the **Comprehensive Modular Survey: Telecom (CMS:T), NSS 80th Round, Jan–Mar 2025** — 34,950 households, 1,42,065 persons:

**Household level:**
- **85.5% of Indian households possess at least one smartphone** (rural 82.1%, urban 91.3%)
- **86.3% have internet access within household premises** (rural 83.3%, urban 91.6%)

**Individual ownership, age 15+ — where it breaks:**

| Indicator (15+) | Rural male | **Rural female** | Urban male | Urban female |
|---|---|---|---|---|
| **Owns a mobile phone** | 80.7% | **48.4%** | 90.0% | 71.8% |
| Used internet in last 3 months | 72.1% | 57.6% | 85.5% | 74.0% |
| Used mobile in last 3 months | 89.5% | 76.3% | 95.0% | 86.8% |
| **Can send a message with an attached file** | 67.2% | **50.9%** | 79.1% | 65.8% |

- Even at 15–24, **rural female mobile ownership is 51.7%** vs rural male 74.8%
- All-India, only **73.4% of people aged 15–29** own a mobile phone
- Among those who *can* bank online, **99.5% use UPI** — UPI literacy is near-universal *conditional on access*

✅ *PIB Release ID 2132330, 29 May 2025 — https://pib.gov.in/PressReleasePage.aspx?PRID=2132330*
✅ *Full report: https://www.mospi.gov.in/sites/default/files/press_release/Final_press%20release_CMS_T.pdf*

> **The killer framing for the deck:**
>
> *"Household smartphone penetration is 85.5%. But fewer than half of rural women over 15 own a phone. Any welfare-transparency app that assumes personal device ownership excludes the single largest group of welfare beneficiaries in the country."*

### A12.2 Literacy ✅

- All-India literacy (7+): **80.9%** (2023-24); **rural 77.5%**
- Rural Rajasthan: male 83.6%, **female 61.8%**. Rural Bihar: male 81.5%, **female 65%**
- ✅ *PLFS 2023-24, MoSPI, via Lok Sabha reply — https://www.sansad.in/getFile/loksabhaquestions/annex/185/AU4441_bSNrYF.pdf*

### A12.3 Language ✅

- **43.63% of Indians report Hindi (incl. Bhojpuri etc.) as mother tongue** per Census 2011 — **~56% do not.** ✅ `https://language.census.gov.in/showDashboard`
- ⚠️ **No authoritative current figure for the share of Indians comfortable in English was found.** Census C-17 (bilingualism/trilingualism) holds the raw basis at `https://www.censusindia.gov.in/nada/index.php/catalog/10262`. **Do not cite an English-proficiency percentage.**

✅ **Existing infrastructure to build on:** **Bhashini** translation plugins are already deployed across **eGramSwaraj, LGD, AuditOnline and Meri Panchayat** (the widget is visibly embedded on all four). CPGRAMS runs a **Bhashini-powered multilingual voice chatbot** and supports **all 22 scheduled languages**.

### A12.4 Voice access ✅ — the clearest gap of all

> **No evidence was found of any large-scale, currently-operating inbound IVR or voice-first channel for scheme transparency or grievance filing in India.**
>
> CPGRAMS has an *outbound, post-disposal* Feedback Call Centre and a chatbot. CSC integration extends reach *via intermediaries*. **Inbound voice access to scheme spending data does not exist.**

Every transparency channel found — Meri Panchayat, CPGRAMS, eGramSwaraj, AuditOnline — is **app-or-web-first**. With **51.6% of rural women 15+ not owning a phone** and **49.1% unable to send a file attachment**, the population most affected by leakage has the least access to the portals documenting it.

---

# PART B — THE ACADEMIC STATE OF THE ART

*All arXiv IDs below were retrieved from the arXiv API/search index on 29 July 2026 and title-verified. Where an ID could not be verified for a well-known system, the system is named with **no ID** and this is stated. IDs beginning `25xx`/`26xx` are 2025/2026 submissions.*

## B1. Procurement fraud & collusion detection

**The single most important structural finding: supervised learning is genuinely hard here because there are no confirmed negatives.** You never know that a contract was *clean*; you only ever learn that some were dirty.

| Paper | Contribution | Key result |
|---|---|---|
| **Learning from sanctioned government suppliers: ML and network science in Mexico** — arXiv:2512.19491 (2025), Medina-Hernández, Kertész, **Fazekas** | **Positive-Unlabeled (PU) learning** combining domain red flags + network features on Mexican federal procurement + company sanction records | Best PU model captures **+32% more known positives**, **2.3× better than random**. SHAP shows **network-derived features (core membership, supplier eigenvector centrality) dominate red flags** |
| **Catching Bid-rigging Cartels with Graph Attention Neural Networks** — arXiv:2507.12369 (2025) | GATs on bidding graphs, 13 markets across 7 countries, tests cross-market transfer | **91% average accuracy** cross-market (8 Swiss + Okinawa); **84%** extended to 12 markets; beats traditional ML ensembles |
| **Collusion Detection with Graph Neural Networks** — arXiv:2410.07091 (2024) | Two-phase: per-market training then **zero-shot OOD transfer** to unlabelled markets (Japan, US, Swiss, Italy, Brazil) | Establishes cross-market transfer as feasible |
| **PANG: Pattern Mining for Anomaly Detection in Graphs — Fraud in Public Procurement** — arXiv:2306.10857 (ECML PKDD 2023) | **Explainable induced-subgraph pattern mining**; designed for when red-flag attributes are *missing* from notices | On-par with SOTA on standard benchmarks, **superior on procurement data**, plus interpretable fraud-prone motifs |
| **The Payment Heterogeneity Index (PHI)** — arXiv:2605.12547 (2026) | **Post-award payment** monitoring — unsupervised, interpretable, **no labels needed** | Flags **0.6% of suppliers / 10.1% of high-volume vendors** in UK municipal data as structurally distinct; ρ=0.310 vs Coefficient of Variation (reveals regimes CV hides) |
| **Corruption Risk in Contracting Markets: A Network Science Perspective** — arXiv:1909.08664 (2019), Wachs, Fazekas, Kertész | 4M+ EU contracts 2008–2016 as buyer–supplier bipartite networks | **Centralized markets have higher corruption risk**; risk is clustered, but sits in the *core* in some countries and the *periphery* in others |
| **Validating corruption risk measures** — arXiv:2309.01462 (2023) | Item Response Theory validation of **15 red-flag indicators** on Italy's National Database of Public Contracts | ⚠️ **Red flags are multidimensional and non-superimposable — a single composite "corruption risk index" is statistically unjustified.** |
| **FOPPA: Open Database of French Procurement Award Notices 2010–2020** — arXiv:2305.18317 (*Scientific Data* 2023) | **1,380,965 lots** from TED with documented data-quality repairs | The reference example of how to clean a national tender database |
| **Structural asymmetry as a fraud signature: Heron's Information Coefficient** — arXiv:2511.10957 | Geometric subgraph-deviation measure; 8 years of Brazil SUS medical-supply bidding | Beats other information-theoretic metrics across corruption intensities |
| **ERP-RiskBench: Leakage-Safe Ensemble Learning** — arXiv:2603.06671 (2026) | Nested CV with time- and group-aware splits | **Leakage-safe protocols reduce previously inflated accuracy by a notable margin**; three-way-matching discrepancies are top predictors |
| **Swimming in Dark Water: When Cartels Mimic Competition** — arXiv:2606.30470 (2026) | Forensic reconstruction of a Ticino road-construction cartel 1999–2005 | **Overcharges ≥ 45%**; cartel members **strategically mimicked competitive bidding to evade standard econometric screens** |
| **Organized crime behavior of shell-company networks** — arXiv:2307.10028 (*Trends in Organized Crime* 2023) | Joins contracting + **ownership/management** data | Quantifies economic impact of *connected* vs single shell companies |
| **Detecting bid-rigging coalitions across countries and auction formats** — arXiv:2105.00337 (2021) | Coalition screens + lasso/SVM/RF/super-learner | **~90% correct classification** (Swiss, Japanese, Italian) |
| **Deep learning for bid rigging: CNNs on pairwise bidding graphs** — arXiv:2104.11142 (2021) | Converts pairwise normalized bids into images for a CNN | ~90% within-country; **degrades transnationally** |
| **Flagging Incomplete Bid-rigging Cartels** — arXiv:2004.05629 (2020) | Screens over all 3- and 4-bid subgroups within a tender | Handles the realistic case where only *some* bidders collude |
| **Toward Auditable Fraud Detection: Graph Features + Explanations + Agentic Case Investigation** — arXiv:2607.19266 (2026) | Graph features → explanations → LLM agent case file | **Closest published architecture to "detect + explain + hand to a human investigator"** |

**On the World Bank / DIGIWHIST / Opentender "red flags" methodology:** the canonical objective indicators — *single-bidder rate, tender period shortening, short advertisement periods, non-open procedure type, call-for-tender not published, high supplier market share, weighted Corruption Risk Index* — come from Fazekas and the Government Transparency Institute and are published in **policy/journal channels, not arXiv**. The arXiv papers above *use and validate* that methodology; arXiv:2309.01462 is the strongest evidence that the red-flag set must be treated as **multi-dimensional rather than a single score.**

---

## B2. Graph anomaly detection / GNN fraud

**The most important sanity check in the field:**

> **GADBench: Revisiting and Benchmarking Supervised Graph Anomaly Detection** — arXiv:2306.12251 (NeurIPS 2023 D&B). 29 models × 10 datasets up to ~6M nodes.
> **Headline result: tree ensembles with simple neighborhood aggregation outperform the latest task-specific GNNs.**

That single finding should shape any architecture: **start with LightGBM on graph-derived features; treat the GNN as a challenger that must earn its place.**

**Foundations:**
- **BWGNN — Rethinking GNNs for Anomaly Detection** — arXiv:2205.15508 (ICML 2022). Identifies the **"right-shift" spectral phenomenon** (anomalies push spectral energy to high frequencies); Beta Wavelet band-pass filters.
- **CARE-GNN — GNN Fraud Detectors against Camouflaged Fraudsters** — arXiv:2008.08692 (CIKM 2020). Feature + relation camouflage; label-aware similarity + RL neighbor selection.
- **DGraph: Large-Scale Financial Dataset for GAD** — arXiv:2207.03579 (NeurIPS 2022). ~3M nodes, 4M dynamic edges, 1M ground-truth labels.
- ⚠️ **PC-GNN** and **GAGA** are genuinely important (both in GADBench's comparison) but their arXiv IDs were **not verified** — no ID given here deliberately.

**2025–2026 frontier:**

| Paper | Why it matters |
|---|---|
| **GAD in the Wild: Benchmarking under Realistic Deployment Challenges** — arXiv:2605.07133 | The deployment-realism successor to GADBench |
| **Towards Anomaly Detection on Relational Data** — arXiv:2606.18621 | Moves GAD from a single graph to **multi-table relational databases** — exactly the shape of a government spending DB |
| **Graph-Based Fraud Detection with Dual-Path Graph Filtering** — arXiv:2604.14235 (*Neural Networks*) | |
| **Balanced Anomaly-guided Ego-graph Diffusion for Inductive GAD** — arXiv:2602.05232 (KDD 2026) | **Inductive** — new nodes at test time, i.e. new vendors |
| **LLM-Powered Text-Attributed Graph Anomaly Detection via Retrieval-Augmented Reasoning** — arXiv:2511.17584 | Bridges GNN + LLM explanation |
| **KnowGraph: Knowledge-Enabled Anomaly Detection via Logical Reasoning** — arXiv:2410.08390 (ACM CCS 2024) | **Injects domain logic rules into GNN detection** — the route to encoding procurement law as constraints |

**Money laundering — the closest technical analogue to fund diversion:**

| Paper | Key result |
|---|---|
| **SALT-GNN: Dense Neighborhoods in AML Graphs via Statistics-Aware Attention** — arXiv:2607.10131 | **+3–6 F1** in dense recipient contexts; **+16–20 F1** on highest-degree nodes; **up to 77% fewer parameters** than graph-transformer baselines |
| **TransXion: High-Fidelity Graph Benchmark for Realistic AML** — arXiv:2604.17420 | ~3M transactions / 50K entities **with demographic + behavioral profiles**. Deliberately yields **lower** scores than existing benchmarks — i.e. **prior AML numbers are inflated** |
| **Tide: Customisable Dataset Generator for AML** — arXiv:2603.01863 | LightGBM PR-AUC **78.05** at 0.10% illicit rate; XGBoost **85.12** at 0.19% — **model ranking flips with base rate** |
| **Do Transaction-Level and Actor-Level AML Queues Agree? (Elliptic++)** — arXiv:2604.23494 | At 1% review budget, queue overlap **Jaccard 0.374 / 0.087**. **Scoring granularity changes who gets investigated** |
| **Explainable AML Triage with LLMs** — arXiv:2604.19755 | PR-AUC 0.75, Escalate F1 0.62, **citation validity 0.98**, evidence support 0.88, counterfactual faithfulness 0.76 |
| **RDLI: Knowledge-Integrated Representation Learning under Extreme Label Scarcity** — arXiv:2601.12839 | **+28.9% F1** over SOTA GNNs at **0.01% label rate**; path-level explanations improved expert-rated trust |
| **Clue2Group: Clue-Guided Money Laundering Group Discovery** — arXiv:2606.26189 | Reframes detection as *analyst starts from one clue and expands* — matches how a real audit works |
| ⚠️ **From Accuracy to Auditability: Determinism in Financial AI** — arXiv:2605.23955 | Measures **explanation rank instability, GNN prediction flip rates, tensor-parallel LLM output divergence** — **the same model gives different answers on re-run.** Critical if a citizen can legally challenge a flag |

---

## B3. GraphRAG & knowledge graphs + LLMs

**Foundations (verified):**
- **From Local to Global: A Graph RAG Approach to Query-Focused Summarization** — arXiv:2404.16130 (Microsoft). LLM builds entity KG + pre-generated community summaries; substantially better than conventional RAG on **global sensemaking** over ~1M-token corpora.
- **HippoRAG** — arXiv:2405.14831 (NeurIPS 2024). LLM + KG + Personalized PageRank. **Up to 20% better** on multi-hop QA; single-step retrieval **10–30× cheaper and 6–13× faster** than iterative IRCoT.
- **LightRAG** — arXiv:2410.05779. Dual-level graph+vector retrieval with **incremental update** — matters for a spending DB that changes daily.

**Most directly transferable 2026 work:**

| Paper | Why it matters | Result |
|---|---|---|
| ⭐ **Agentic GraphRAG for Auditable Commercial Registry Analysis** — arXiv:2605.18770 | **The closest published system to what this project builds.** Turns the Swiss Official Gazette of Commerce (millions of records: structured metadata, multilingual legal notices, temporal events, **entity aliases**) into a Neo4j graph with tool-mediated, **auditable** natural-language analysis | Existence proof at national-registry scale |
| **LLM-Guided Planning for Multi-hop Reasoning over Nuclear Regulatory Documents** — arXiv:2606.29399 (ICML 2026 wksp) | Head-to-head on a regulatory corpus | **81.5%** vs 43.5% baseline (+38.0pp); beats **LightRAG 73.0%, HippoRAG 70.5%, GraphRAG 49.5%** |
| **QO-Bench: Query-Operator-Preserving Retrieval over Typed Event Tuples** — arXiv:2606.04646 | Compares RAG / ReAct RAG / GraphRAG / **IE-to-SQL** with **operator-level diagnosis (joins, intersections)** | Exactly the "aggregate spending across districts" failure mode |
| ⚠️ **Ex-GraphRAG: Interpretable Evidence Routing** — arXiv:2605.21994 | **Message-passing GNN encoders entangle node contributions so you cannot faithfully audit which entity drove the answer.** Directly relevant to citizen-facing explanations | |
| **Why Neighborhoods Matter: Traversal Context and Provenance in Agentic GraphRAG** — arXiv:2605.15109 | Frames **citation faithfulness as a trajectory-level problem** | |
| **HEAR: Hypergraph Enterprise Agentic Reasoner** — arXiv:2605.14259 | Argues both GraphRAG *and* NL2SQL "lack the semantic grounding and **auditable execution**" needed for multi-hop reasoning | |
| **Is GraphRAG Needed?** — arXiv:2606.25656 (ACL 2026 GEM) | Honest scoping framework for *when* graph structure actually helps | |
| **Format-Constraint Coupling in KG Construction from Statistical Tables** — arXiv:2605.21974 | KG extraction quality from **statistical tables** is coupled to surface format / column-name anchoring — **a real hazard when ingesting government CSV/XLSX** | |
| **IndicRAGSuite** — arXiv:2506.01615 (AI4Bharat) | **IndicMSMarco**: 1000 MS MARCO queries manually translated into **13 Indian languages**; (question, answer, passage) tuples from **19 Indic Wikipedias** | |
| **Robust Interpretation of Historical Documents in KGs Through Query Inference** — arXiv:2607.24475 (ICDAR 2026) | Compares RAG vs agentic GraphRAG **specifically under OCR and transcription errors** — the exact regime of scanned Indian government records | |

---

## B4. Indic NLP and speech

**Short answer to "is voice in 10+ Indian languages feasible today?": yes for text/translation, yes for clean read speech, and marginally for noisy rural conversational audio. Here are the numbers.**

| Paper | Coverage | Key result |
|---|---|---|
| **IndicTrans2** — arXiv:2305.16307 (TMLR 2023, AI4Bharat) | **All 22 scheduled languages** | Releases **BPCC: 230M bitext pairs** (126M new, 644K human-translated) + first **n-way parallel benchmark** covering all 22 with India-origin content. **Open weights, permissive license** |
| **IndicVoices** — arXiv:2403.01926 | **22 languages, 145 districts** | **7,348 hours** from **16,237 speakers** — 9% read, **74% extempore, 17% conversational**. Trains IndicASR, first ASR supporting all 22 scheduled languages |
| **Vistaar / IndicWhisper** — arXiv:2305.15386 (Interspeech 2023) | 12 languages, 59 benchmarks | **Lowest WER on 39 of 59 benchmarks**, average reduction **4.1 WER** |
| **Shrutilipi** — arXiv:2208.12666 | 12 languages | **6,400+ h** mined from All India Radio. **WER drops 5.8% avg** across 7 languages; **Hindi 18.8% → 13.5%** |
| **IndicSUPERB / Kathbath** — arXiv:2208.11761 | 12 languages, 203 districts | 1,684 h labelled, 1,218 contributors, 6 tasks |
| ⭐⚠️ **Benchmarking ASR for Indian Languages in Agricultural Contexts** — arXiv:2602.03868 (2026) | Hindi, Telugu, Odia | **THE most decision-relevant number in this document for voice UX.** 10,934 real field recordings × up to 10 ASR models. **Best Hindi WER 16.2%. Best Odia WER 35.1%, and only achievable with speaker diarization.** Diarization + best-speaker selection cuts WER by **up to 66%** on multi-speaker audio |
| **Jointly Improving Dialect ID and ASR in Indian Languages** — arXiv:2607.02862 | **8 languages, 33 dialects** | Dialect-ID accuracy **81.63%**; avg **CER 4.65% / WER 17.73%** |
| ⚠️ **Impact of region-specific data on Indic ASR** — arXiv:2606.09345 | Cross-*district* generalization | **Consistent correlation between inter-district geographic distance and WER** — a model trained in one district degrades measurably in the next |
| ⚠️ **Script collapse in multilingual ASR** — arXiv:2604.08786 | 10 languages, 10 models | Introduces **Script Fidelity Rate (SFR)**. **21 of 100 model-language pairs collapse (SFR<10%)** — fluent output in the **wrong script, invisible to WER**. Includes Devanagari substitution for Bengali/Malayalam. **Script-aware prompting: mean SFR 71.2% → 97.7%; Urdu 6.5% → 97.0%** |
| **IndicContextEval** — arXiv:2606.19157 (Interspeech 2026) | 8 languages, 23 domains | 56 h, 555 speakers; tests whether AudioLLMs actually *use* provided entity lists or fall back on parametric knowledge |
| ⚠️ **IndicIFEval** — arXiv:2602.22125 | **14 Indic languages** | Models follow *formatting* constraints well but **struggle badly on lexical and cross-lingual constraints**; Indic instruction-following lags English substantially |
| **IndicBERT v2 / IndicCorp v2 / IndicXTREME** — arXiv:2212.05409 (ACL 2023) | **24 languages** | 20.9B token monolingual corpus; IndicXTREME = 9 NLU tasks × 20 languages |
| ⭐ **Aksharantar / IndicXlit** — arXiv:2205.03018 (EMNLP Findings 2023) | **21 languages, 12 scripts** | **26M transliteration pairs** (21× larger than prior); **+15% accuracy** on Dakshina. **Essential for name matching** |
| **RomanSetu** — arXiv:2401.14280 (ACL 2024) | Romanized interface | Romanization **reduces token fertility 2–4×** and matches/beats native script |
| **Airavata: Hindi Instruction-tuned LLM** — arXiv:2401.15006 (AI4Bharat) | Hindi | OpenHathi + IndicInstruct |
| **Krutrim LLM** — arXiv:2502.09642 | Indic | 2T tokens; matches/exceeds LLaMA-2 on **10 of 16 tasks** at far lower training FLOPs |
| **WWHO / SGPE syllable-aware tokenization for Abugida scripts** — arXiv:2603.25309 | Hindi/Sanskrit/Sinhala | Hindi **TWR 1.181 = 27.0% token reduction vs o200k**; quantifies the **"Token Tax" for the Global South** |
| **CoSTA: Code-Switched Speech Translation** — arXiv:2406.10993 | Bn/Hi/Mr/Te–English | **+3.5 BLEU** over cascaded and end-to-end baselines |

⚠️ **Sarvam AI:** searched arXiv for `ti:"Sarvam"` — **no paper found.** Sarvam's models (Sarvam-M, Sarvam-1, Shuka, Saaras) are released via model cards/blog posts, **not arXiv**. Do not cite an arXiv ID.
⚠️ **Bhashini** is a MeitY government programme, not an arXiv publication; its underlying ASR/MT models are largely the AI4Bharat stack above.

---

## B5. Document AI / OCR on messy government paper

| Paper | Contribution | Key result |
|---|---|---|
| **olmOCR** — arXiv:2502.18443 (AI2) | Open 7B VLM + full pipeline, trained on 260K pages from 100K+ crawled PDFs incl. **handwritten text and poor scans**; releases olmOCR-Bench (1,400 hard PDFs) | Converts **1M PDF pages for $176** (vs >$6,240 for GPT-4o); outperforms GPT-4o, Gemini Flash 2, Qwen-2.5-VL |
| **General OCR Theory (GOT) — OCR-2.0** — arXiv:2409.01704 | 580M-param unified end-to-end: plain text, formulas, **tables**, charts, sheet music; region-level recognition by coordinate/colour prompt | |
| ⭐⚠️ **Can OCR-VLMs Read Devanagari? A Stress-Test Benchmark** — arXiv:2606.29213 (2026) | **10 systems** on Devanagari/Hindi: EasyOCR, Qwen2.5-VL-3B, Qwen3-VL-8B, olmOCR-7B, DeepSeek-OCR, Gemini 2.5 Flash, Claude Opus 4.7, GPT-5.5, Mistral OCR; 4 synthetic degradations + **300 real printed scans** | **On clean synthetic text all 10 cluster at chrF++ 91–98. On REAL scans, nine of ten collapse:** EasyOCR **93.6 → 58.3**; **GPT-5.5 → 58.5** (ties classical EasyOCR); **olmOCR-7B → 40.5**; open **Qwen3-VL-8B 75.2** (one 24 GB GPU); **Gemini 2.5 Flash 86.3**; **Claude Opus 4.7 82.2**. DeepSeek-OCR shows catastrophic repetition (up to **71× reference length**). Errors concentrate in **conjuncts, matras, nukta** — exactly the marks that distinguish names |
| **Barnamala: Parameter-Efficient Handwritten Devanagari** — arXiv:2607.13689 | 1.11M-param CNN on 46-class DHCD | **99.73%** — highest reported, **15.6× smaller** than prior SOTA. Every model hits the same **11-error intrinsic floor** = benchmark saturated |
| ⭐⚠️ **Handwriting Extraction of Signature Lists in Swiss Popular Initiatives** — arXiv:2606.05018 (ICCST 2026) | **The single best analogue for muster rolls.** 443 handwritten entries, 418 writers | OCR **CER 29.6% for first names** — off-the-shelf OCR is **not reliable** for short handwritten names. **But writer retrieval reaches mAP 50.6%** and is effective for **detecting duplicate submissions via handwriting similarity** — i.e. detecting *the same hand filling many rows* |
| ⚠️ **Do VLMs Read or Rewrite? Transcription Faithfulness in VLMs** — arXiv:2607.21617 | Whether VLMs silently "correct"/paraphrase what they read | **A fatal failure mode for evidentiary documents** |
| **DRISHTIKON: Visual Grounding at Multiple Granularities in Documents** — arXiv:2506.21316 (IIT Bombay) | Grounding answers to specific document regions | Needed so a citizen can **see where the number came from** |
| **MADP: Multi-Agent Pipeline for Document Processing with Human-in-the-Loop** — arXiv:2605.17159 | Production deployment on **955 real documents** | **97.0% full-pipeline automation, 98.5% document-level accuracy** with HITL on a stratified 100-doc subset |
| **FinCriticalED: Visual Benchmark for Financial Fact-Level OCR** — arXiv:2511.14998 | Evaluates OCR at the level of **whether the extracted number is right** — the correct metric for bills/UCs | |
| **PaddleOCR 3.0** — arXiv:2507.05595 | **Apache-2.0** — the realistic free baseline | |
| **HW-MLVQA** — arXiv:2507.15655 (IIIT-H) · **NoTeS-Bank** — arXiv:2504.09249 · **Infinity Parser** — arXiv:2506.03197 · **Seeing Straight (orientation)** — arXiv:2511.04161 · **Khondo (Bangla form packet splitting)** — arXiv:2607.21780 | Supporting toolchain | |
| **A Survey of OCR Evaluation Methods and the Invisibility of Historical Documents** — arXiv:2603.25761 (FAccT 2026) | Argues current OCR metrics **systematically hide failure on non-Latin/degraded documents** | |

⚠️ **LayoutLMv3 / Donut / Nougat / DocLayout** are real and widely used, but their arXiv IDs were **not verified** in this pass — no IDs cited.

---

## B6. Entity resolution

| Paper | Contribution | Key result |
|---|---|---|
| **Ditto: Deep Entity Matching with Pre-Trained LMs** — arXiv:2004.00584 (VLDB 2021) | The reference transformer EM system | **+29% F1** over prior SOTA; **96.5% F1** matching two real company datasets (**789K × 412K records**); reaches prior SOTA with **half the labels** |
| **(Almost) All of Entity Resolution** — arXiv:2008.04443 (Binette & Steorts) | The standard survey | Read before designing anything |
| **How to Evaluate Entity Resolution Systems: An Entity-Centric Framework** — arXiv:2404.05622 | Fixes the **pairwise-F1 evaluation trap** that inflates ER numbers | |
| ⭐ **d-blink: Distributed End-to-End Bayesian Entity Resolution** — arXiv:1909.06039 (JCGS 2020) | Bayesian ER with **calibrated uncertainty**; includes a **2010 U.S. Decennial Census case study** | **Proven at government-register scale** |
| **Bayesian Graphical ER Using Exchangeable Random Partition Priors** — arXiv:2301.02962 (*JSSAM* 2023) | | |
| **Progressive Entity Resolution: A Design Space Exploration** — arXiv:2503.08298 (ACM) | **Anytime ER** — produce matches under a budget | Exactly what an audit queue needs |
| **Transformer-Gather, Fuzzy-Reconsider** — arXiv:2509.17470 (ICCKE 2025) | Embedding retrieval + fuzzy re-ranking | The pragmatic 2025 recipe |
| **A Robust Pipeline for Enterprise-Level Large-Scale ER** — arXiv:2508.03767 | Production engineering | |
| **BlockingPy: ANN blocking for record linkage** — arXiv:2504.04266 | Open-source ANN blocking | The scalability bottleneck |
| ⭐ **Optimal Transport-based Alignment of Learned Character Representations for String Similarity** — arXiv:1907.10165 (ACL 2019) | **The relevant method for transliterated/variant-spelling names** — character-level, learned, alignment-aware | |
| **Single and Multi Truth Data Fusion using LLMs** — arXiv:2606.28062 | LLM prompting for truth discovery over conflicting tabular sources | **Outperforms classical unsupervised truth discovery (DART, LTM) on all three benchmarks** |

> ⚠️ **Verified hole in the literature.** A targeted search for 2025–2026 arXiv work on **privacy-preserving record linkage (PPRL)** and on **Indian name matching / duplicate detection for Indian names** returned **only 22 total results** for "entity resolution record linkage", **none PPRL-focused post-2023, and no dedicated Indian-name ER paper.** See Gap 4 in Part D.

---

## B7. LLM agents over structured data — reliability

**This is where expectations should be set lowest and the design should be most defensive.**

| Paper | Contribution | Key result |
|---|---|---|
| **BIRD: Can LLM Already Serve as A Database Interface?** — arXiv:2305.03111 (NeurIPS 2023) | Realistic text-to-SQL: 12,751 pairs, 95 DBs, 33.4 GB, 37 domains, **dirty database contents** | ChatGPT **40.08% execution accuracy vs human 92.96%** |
| ⭐⚠️ **What Predicts Correctness in Text-to-SQL? A Selective-Prediction Study** — arXiv:2607.06799 (2026) | **The most important reliability paper here.** Which signals predict whether generated SQL is right | Black-box signals (string/structural/execution self-consistency, schema relevance, executability) all sit at **0.61–0.68 AUROC**; white-box log-prob 0.67. **LLM-judge: 0.72 → 0.78 (Claude); two-provider judge ensemble → 0.82 AUROC, ECE 0.03.** Practical operating point: **answer 27% of questions at 24% selective risk.** Fine-tuned verifiers reach 0.77–0.79 in-domain but **fall to ~0.66 on unseen schemas**; scaling to 7B, schema diversity, distillation, and cross-benchmark training **all fail to close the gap** |
| ⭐ **How Far Do On-Prem Open LLMs Get on Text-to-SQL?** — arXiv:2606.29733 (2026) | Reproducible, McNemar-tested ablation of the standard "accuracy recipe" | Qwen2.5-Coder **7B: 39.1 EX**; Llama-3.3-70B **49.2 EX**. **Self-correction is a robust near-free win. Schema linking does NOT help** — even a retrieval linker with **96.5% gold-table recall** is statistically indistinguishable from no linking. **Self-consistency is poor value: +0.13pp for ~5× tokens (not significant)** |
| **Spider 2.0-AIFunc** — arXiv:2607.06229 | 465 verified instances, 125 real enterprise DBs | Best proprietary **67–70% EX**; best open-source **58.1%**. **Elaborate agent frameworks do not beat a minimal agent** |
| ⭐⚠️ **AuthentiCity: Provenance-Aware KG + Benchmark** — arXiv:2607.25243 | 180M nodes / 220M edges across 5 cities; NL→query with **provenance-aware filtering, cross-source agreement/disagreement, coverage-aware aggregation, infeasible-query detection** | Strong commercial LLM reaches only **54–69% execution accuracy**; a **7B open model 6–19%**, and **the open model never abstains on unanswerable questions** |
| **DBCC: Database Context Compression** — arXiv:2606.28601 | Argues the bottleneck is **database representation**, not reasoning | Input **2.6M → 34.7K tokens**; schema-linking strict recall **0% → 56.5%** |
| **Schema-First Retrieval: Embedding Catalogs** — arXiv:2606.28387 | Indexes catalog metadata rather than rows | **96.4% table recall@20**; query history raises SEDE recall@5 **52.1% → 92.3%**; BIRD SQL execution errors **15.6% → 6.2% (2.5×)** |
| **GradeSQL: Test-Time Verification via Outcome Reward Models** — arXiv:2606.30851 | Task-specific ORM via execution-based labelling | **+4.33% BIRD, +2.10% Spider** over Best-of-N and Majority Voting |
| ⭐ **Benchmarking Text-to-SQL under Role-Based Access Control** — arXiv:2607.22115 (SIGMOD 2027) | **Essential for beneficiary data** | Many high-scoring systems — **especially open-weight LLMs** — **degrade sharply** once access constraints exist, through frequent RBAC violations |
| **PCC-SQL: Policy-Conditioned Constrained Decoding for Column-Level Access Control** — arXiv:2607.12341 | Per-token logits masking tied to grammar productions | **0% leakage rate**, coverage up to **88.7%** |
| **ABISS: Evaluating Text-to-SQL Through Agent Interaction** — arXiv:2607.23340 | Ambiguous/unanswerable taxonomy + simulated multi-turn users | Models **detect** a problematic question but **cannot pinpoint the subcategory**; even after clarification they often still fail |
| **FinRule-Bench: Joint Reasoning over Financial Tables and Principles** — arXiv:2603.11339 | Rule verification / identification / **multi-violation diagnosis** | Good on **isolated rule verification**, degrade **sharply** on rule discrimination and multi-violation diagnosis — **exactly the audit task** |
| **Self-Consistency Improves CoT** — arXiv:2203.11171 (ICLR 2023) | The canonical method | GSM8K +17.9% — **but see 2606.29733: buys almost nothing on text-to-SQL** |
| ⭐⚠️ **FBI: Finding Blind Spots in Evaluator LLMs** — arXiv:2406.13439 (EMNLP 2024, **AI4Bharat**) | 2,400 deliberately perturbed answers, 22 perturbation categories, 5 evaluator LLMs | **Evaluator LLMs fail to identify quality drops in over 50% of cases on average.** Reference-based evaluation is notably better |
| **A Survey on LLM-as-a-Judge** — arXiv:2411.15594 | Reliability strategies + judge-reliability benchmark | |
| **Agents That Know Too Much: Privacy in LLM Agents** — arXiv:2606.26627 | Taxonomy of leakage via queries, intermediate results, memory writes, inter-agent messages | Only **information-flow control** covers compositional and cross-session inference leakage |

> ### The single most important engineering conclusion in this entire document
>
> Given: NL→query execution accuracy is **54–69%** for strong commercial models on provenance-aware graphs and **6–19%** for 7B open models which **never abstain**; and the best correctness verifier reaches **0.82 AUROC** only at an operating point that **answers 27% of questions**…
>
> **…you cannot let an LLM write queries against a citizen-facing government spending database.**
>
> The architecture must be an **intent-classification → parameterised-query-template router**, not free-form text-to-SQL. ~40 hand-written, unit-tested, parameterised queries covering the top 95% of citizen questions. The LLM's *only* jobs are (a) classify intent, (b) extract slots, (c) phrase the answer in the user's language. This converts a 60%-accuracy problem into a >95%-accuracy problem and makes every answer reproducible and auditable.

---

## B8. Satellite & computer vision for asset verification

### B8.1 Can you verify from space whether a road/pond/toilet/house exists?

**The honest answer, backed by 2026 evidence: partially, with sharp and quantified limits.**

| Paper | Contribution | Key result |
|---|---|---|
| ⭐⚠️ **Land cover and flood type govern the detection limits of satellite-based mapping** — arXiv:2606.07780 (2026) | Deploys **Prithvi-EO-2.0** across **19 out-of-distribution events**, 6 continents, 8 climate zones, validated against 2 independent reference products | **Cropland IoU 52%; riverine F1 0.69. Tree cover and BUILT-UP areas: near-zero detection, IoU ≈ 4%.** Apparent model error is partly **definitional inconsistency between reference products**; **23 failure modes** identified where **pipeline engineering dominated model capacity** as an error source. **The strongest published caution against naïvely trusting a GFM to see built assets** |
| ⭐⚠️ **EarthShift: robustness to real-world distribution shifts in EO** — arXiv:2605.29330 | 8 geospatial foundation models × 11 tasks × 5 shift types | **GFMs perform 15–20% worse out-of-distribution on average, regardless of architecture, size, pretraining, or fine-tuning strategy** — and no better than generic vision FMs |
| ⭐⚠️ **No One Knows the State of the Art in Geospatial Foundation Models** — arXiv:2605.12678 | **152-paper audit** | **46 cross-paper disagreements of ≥10 points** for the *same* model/benchmark/protocol; **94 of 126** papers use a unique pretraining config; **39% release no weights** |
| **Prithvi-EO-2.0** — arXiv:2412.02732 (NASA–IBM) | 4.2M global time-series samples from Harmonized Landsat & Sentinel-2 at **30 m** | **+8% over Prithvi-EO-1.0**; beats 6 other GFMs across 0.1 m–15 m. **Open on HuggingFace / TerraTorch** |
| **TerraMind** — arXiv:2504.11171 (ICCV 2025, ESA Φ-lab + IBM) | First **any-to-any generative** multimodal EO foundation model, 9 modalities; "Thinking-in-Modalities" generates missing sensors at inference | Beyond-SOTA on PANGAEA; **fully open-sourced, permissive license** |
| **TerraMind vs THOR systematic comparison** — arXiv:2607.18504 | Controlled ablation across 10 use cases | **Patch size and decoder type explain more performance variance than model identity** |
| **Benchmarking GFMs for Agriculture** — arXiv:2606.29664 | Prithvi, SpectralGPT, SatMAE with **region-disjoint splits** | **All three degrade sharply under regional shift**, predicting only common classes |

### B8.2 Change detection — the actual mechanism for "did the asset get built?"

| Paper | Key result |
|---|---|
| ⭐ **SST-CD: Spatially Selective Self-Training for Unsupervised Building Change Detection** — arXiv:2606.10775 | **Label-free.** **F1 83.08% (LEVIR-CD), 91.69% (WHU-CD), 86.60% (DSIFN-CD)** — outperforms all prior unsupervised baselines. **Critical because there is no labelled Indian building-change data** |
| **FAF-CD: Frequency-Aware Fusion under Imperfect Multimodal RS** — arXiv:2606.03114 | Handles **asynchronous, cross-sensor, seasonally shifted** pairs (EO+SAR). **0.924 cF1 LEVIR-CD, 0.955 cF1 WHU-CD** |
| **ChangeRWKV: Linear-Time Change Detection** — arXiv:2603.19606 | **85.46% IoU / 92.16% F1 on LEVIR-CD** at drastically reduced params & FLOPs — the efficiency frontier for national-scale monitoring |
| **ChangeFlow: Latent Rectified Flow** — arXiv:2605.15375 | Average **F1 80.4%** across SYSU/LEVIR/CLCD/OSCD; **65.9 F_scd** on SECOND |
| ⭐ **Seg2Change: Open-Vocabulary Semantic Segmentation for Change Detection** — arXiv:2604.11231 | **+9.52 IoU WHU-CD, +5.50 mIoU SECOND.** **Lets you query changes by arbitrary category name ("pond", "road") without retraining** |
| **MemOVCD** — arXiv:2604.26774 · **ReA-OVCD** — arXiv:2606.20032 · **CoRegOVCD** — arXiv:2604.02160 | **Training-free** open-vocabulary change detection; ReA-OVCD **+2.13 to +9.75 F1**; CoRegOVCD **+2.24 to +4.98 F1**, **47.50% F1 six-class avg on SECOND** |
| **MSI-Net / TUE-CD** — arXiv:2606.10329 | Handles **short imaging intervals with different look angles** — the practical case for revisit-based verification |
| **Delta-QA / Delta-LLaVA: Unifying RS Change Detection and Understanding with MLLMs** — arXiv:2604.14044 | **180k VQA samples**, bi- and tri-temporal, pixel-level segmentation + VQA — the **"explain the change in words to a citizen"** capability |
| **TERRA-CD** — arXiv:2605.14651 | **5,221 Sentinel-2 pairs (2019 vs 2024), 232 cities**, 13-class semantic change |
| **On-board RS Foundation Models for Unsupervised Change Detection** — arXiv:2606.27018 | **Training-free** latent-space anomaly detection between orbital passes |
| ⚠️ **ObliCity: Roof-to-Ground Projection Displacement Correction** — arXiv:2607.25210 | Oblique imagery systematically offsets roofs from footprints — **matters if checking whether the house is on the right plot** |
| ⭐ **Embeddings-based Anomaly Detection for Cleaning Crop Reference Datasets** — arXiv:2607.23908 | Uses GFM embeddings to find **mislabelled/misplaced ground-truth records** — **directly transferable to auditing government asset registers.** **AUROC up to 0.84**; concentrates injected label errors **2.5–5× above chance** |
| **SpaceNet** — arXiv:1807.01232 | The reference open building-footprint / road-network extraction benchmark |
| **Automated National Urban Map Extraction** — arXiv:2404.06202 | National-scale rooftop mapping for countries lacking governance means to maintain one |
| **Tempov: satellite foundation model for wealth monitoring** — arXiv:2604.23166 (Ermon/Burke/Lobell) | 3M bi-temporal **Landsat** pairs; Africa-wide **R² = 0.63**; competitive with only **10% of survey samples** |
| ⚠️ **GFM embeddings improve population estimation unevenly** — arXiv:2605.01650 | **+20.1% median** reduction in unexplained variance — **but gains are uneven and break down predictably under spatial scale mismatch** |

### B8.3 Free/open imagery — the physical limits

Well-established sensor facts:

| Source | Resolution | Revisit | Cost |
|---|---|---|---|
| **Sentinel-2 (ESA Copernicus)** | **10 m** (B2/B3/B4/B8 = RGB+NIR), 20 m red-edge/SWIR, 60 m atmospheric | **~5 days** (S2A+S2B) | **Free** |
| **Landsat 8/9 (USGS/NASA)** | 30 m multispectral, 15 m panchromatic | 16 days per satellite | **Free** |
| **Planet NICFI Basemaps** | ~4.77 m | Monthly | Free but **tropics-only**, program-dependent terms |
| **Bhuvan / ISRO** | Free browse imagery + thematic layers | — | Higher-res Cartosat is **licensed, not open** |
| **Google Earth Engine** | Free compute over Sentinel/Landsat archives | — | Research/non-commercial |

> ### ⭐ The hard physical limit that must be stated openly in the pitch
>
> At **10 m GSD, a single pixel is 100 m².**
>
> | Asset | Visible from free satellite? |
> |---|---|
> | Rural toilet (~1.5 × 1.5 m) | ❌ **Physically invisible** |
> | Hand pump | ❌ **Physically invisible** |
> | Single house extension | ❌ **Physically invisible** |
> | Road (linear, tens of m wide over km) | ✅ **Yes** |
> | Farm pond / check dam | ✅ **Yes** — strong spectral water signature (NDWI) |
> | Land levelling / bunding | ✅ **Yes** |
> | Cluster of new houses | ✅ **Yes** |
>
> **This is a hard physical limit, not a modelling limit.** No amount of AI fixes it. Any pitch that claims to verify toilets from free satellite imagery is lying, and a technical judge will catch it. The correct design response is to **scope satellite verification to large linear/areal assets only**, and to route small assets to the citizen-verification channel.

---

## B9. On-device / edge AI

| Paper | Contribution | Key result |
|---|---|---|
| **Gemma 3 Technical Report** — arXiv:2503.19786 | 1B–27B open multimodal, **128K context**, reduced KV-cache | Gemma3-4B-IT competitive with Gemma2-27B-IT |
| ⭐ **Phi-4-Mini / Phi-4-Multimodal** — arXiv:2503.01743 | 3.8B params, 200K vocab (multilingual), GQA; text+vision+speech via **Mixture-of-LoRAs** | **Ranked first on the OpenASR leaderboard with only a 460M-parameter speech/audio LoRA** — strongest evidence that on-device multilingual ASR is realistic |
| ⭐⚠️ **The Constraint Tax: Validity-Correctness Tradeoffs in Structured Outputs for SLMs** — arXiv:2605.26128 | **The most operationally important on-device paper here.** 15,000 generations on Qwen2.5-0.5B/1.5B, SmolLM2-1.7B | Hard schema decoding raises schema validity **61.5% → 100.0%** but **drops answer accuracy 19.7% → 11.0%** and raises **wrong-but-valid-schema outputs 49.5% → 88.9%**. On a deterministic tool-call task, Qwen2.5-1.5B gets **91.5% executable accuracy with prompt-only JSON but only 48.0% under a hard tool-call schema** — both 100% schema-valid. **The error is semantic, not structural.** Recommended pattern: **reason free, constrain late** |
| ⭐⚠️ **Less Is More: Engineering Challenges of On-Device SLM Integration** — arXiv:2604.24636 | Longitudinal case study, production Android app, Gemma 2.6B + Qwen3 0.6B, 204 commits | Five failure categories: output format violations, constraint violations, context quality degradation, latency incompatibility, model selection instability. **Conclusion: "the most reliable on-device LLM feature is one where the LLM does the least."** |
| **CORE: Lightweight Prompt Compression for QA on Edge** — arXiv:2606.20571 | Deployed on Jetson AGX Orin **and a Huawei Nova smartphone** | Within 2000-token budget: **+30.19% accuracy, −50.47% memory, 1.94× speedup**; vs LLMLingua2 **95.74% energy reduction on the phone** |
| ⚠️ **The Fine-Tuning Trap: Negative Transfer and PEFT in Sub-1B Reasoning** — arXiv:2606.06920 | 5 sub-1B models, 135M–1B | **Full fine-tuning actively harms models under 300M**, often below zero-shot. **PEFT is a stability requirement, not an efficiency preference** |
| **CONCORD: Device-Cloud RAG under Document Isolation** — arXiv:2606.15179 (IEEE ICWS 2026) | Private docs on device, public knowledge in cloud, **no raw document exchange** | **1.66–2.15× throughput**; **>2 orders of magnitude** less per-token communication |
| **SQuaD-SQL: Text-to-SQL with SLMs via LLM-Guided Distillation** — arXiv:2607.08161 | Full training on a **single consumer GPU** | **86.9% execution accuracy on WikiSQL** |
| **How Small Can You Go? LoRA Rank/Quantization for Text-to-SQL on 60M** — arXiv:2607.25583 | T5-small (60M) on WikiSQL | LoRA r=16: **59.6% EM vs 71.2% full FT**, <1% trainable params. **QLoRA INT8 52.8% / NF4 53.2% at 0.60 GB** |
| ⚠️ **Bridging the Reasoning Gap in Vietnamese with SLMs** — arXiv:2604.17794 | Qwen3-1.7B on a low-resource language | **ReAct imposes a "cognitive tax" on 1.7B models** and degrades performance vs plain CoT. Direct analogue for Indic SLM agents |
| ⚠️ **Locale-Conditioned Few-Shot Prompting for On-Device PII Substitution** — arXiv:2605.13538 | **Honest negative finding** | Naive fixed few-shot: the 1-bit SLM **regurgitates demonstration outputs verbatim regardless of input**. Downstream NER F1: **redaction 0.000, faker 0.656, original 0.960** |

⚠️ **On "Gemma 3n":** no separate arXiv paper exists. Released via Google model cards / Kaggle / HF. Cite Gemma 3 (arXiv:2503.19786) and describe 3n's per-layer-embedding / MatFormer design as documented in the model card, **not** as a preprint.

---

## B10. Crowdsourcing integrity & image forensics

| Paper | Contribution | Key result |
|---|---|---|
| ⭐ **DARTIC: Decentralized Anonymous Reputation at Scale** — arXiv:2605.18146 | Dual-ledger; distinct pseudonyms per interaction with **unlinkability + accountability**; **zkSNARK set-membership proofs bind all pseudonyms to one access token** to stop Sybil and reputation-reset attacks | Individual proof gen **<3 s**; aggregation cuts verification of 1024 proofs from **8.7 s → 0.96 s**; zk-batching lowers gas **>100×** |
| **Single and Multi Truth Data Fusion using LLMs** — arXiv:2606.28062 | LLM prompting for truth discovery | **Outperforms DART and LTM across all three benchmarks** |
| **Grading the Narrators: Isnad-Rijal Framework for Claim-Level Provenance** — arXiv:2607.24117 | Transmission-chain provenance with **graded per-domain transmitter reliability**, weakest-link chain evaluation, independent-chain corroboration; serve/review/quarantine routing. 20,000 claims | **Weakest-link quarantine and independent-chain corroboration validated**; paper is explicit that **the grade-recovery loop failed.** Unusually honest |
| ⚠️ **Quotient Semivalues for False-Name-Resistant Data Attribution** — arXiv:2605.07663 | **Proves an impossibility:** exact Shapley-fair attribution over reported identities is **incompatible** with unrestricted false-name-proofness | Manipulation gain drops **1.74 → 0.96** with clustering-based quotient semivalues |
| ⭐⚠️ **Concave is the New Linear: Impossibility of Anti-Plutocratic DAO Governance** — arXiv:2605.18990 | **Proves that no voting rule deriving power solely from a splittable resource resists Sybil splitting** on a permissionless system | Replaying 10 proposals across 5 major DAOs: **Sybil amplification 1,172×–4,039× under Quadratic Voting**, >229,000× under steeper rules |
| **Autonomous FAIR Digital Objects** — arXiv:2605.10370 | Reputation-and-confidence-weighted agreement with a bounded adversarial model | **Resolves 56.3% of 3,914 naturally occurring ClinVar conflicts** later adjudicated by an expert panel. Degrades gracefully **within f < n/5** |
| **CMT: Crowdsourcing Fraud Detection over Heterogeneous Temporal Graph** — arXiv:2308.02793 (DASFAA 2024) | Contrastive multi-view learning for click-farm / paid-report fraud |
| ⚠️ **A Failure-Mode Benchmark for Polymorphic Sybil Poisoning in RAG** — arXiv:2607.03739 | **Threat model if citizen reports feed a RAG index.** *Polymorphic Sybil poisoning*: S lexically diverse passages jointly support an attacker target, evading near-duplicate filters | **+18.8pp hijack amplification**; monomorphic copies register only 4.0% hijack, **polymorphic 22.8% — a 5.7× amplification.** Catching the residual with E5 cosine raises FPR **9×** |

**Image forensics — verifying a citizen's uploaded evidence:**

| Paper | Key result |
|---|---|
| ⭐⚠️ **AEGIS: Holistic Benchmark for Forensic Analysis of AI-Generated Images** — arXiv:2604.28177 (ACL 2026) | **Read this before promising deepfake detection.** 25 MLLMs + 9 expert detectors: **GPT-5.1 reaches only 48.80% overall**; expert models achieve **IoU 30.09%** localization; **11 of 25 generators yield average forensic accuracy below 50%**. Best binary authenticity detection peaks at **79.54%** |
| ⭐ **DINOv3 Beats Specialized Detectors: A Simple Foundation Model Baseline for Image Forensics** — arXiv:2604.16083 | **+17.0 pixel-level F1** over prior SOTA on 4 benchmarks with only **9.1M trainable params** on a frozen ViT-L. Under data-scarce MVSS-Net protocol, LoRA reaches **F1 0.774 vs 0.530**. Robust to Gaussian noise, JPEG recompression, blur |
| ⭐ **FLiD: Field-Localized Forgery Detection for Digital Identity Documents** — arXiv:2605.09089 | **Directly applicable to uploaded ID cards / bills.** **AUC 0.880 (face), 0.954 (text), 0.923 (both-field)**; **29–35pp absolute improvement** over full-document baselines; only **191K trainable params, 13× fewer params and 21× fewer FLOPs** than TruFor/MMFusion/UniVAD |
| **SARIF: Segment Anything for Robust Image Forensics** — arXiv:2606.21108 (ECCV 2026) | Cross-dataset generalization + robustness to compression |
| **Chroma Clues: Color Statistics to Detect Synthetic Images** — arXiv:2606.02224 | **93.27% average generalization accuracy**, interpretable, robust against six post-processing types |
| **Images as Tables: TabPFN for Low-Data Detection of AI-Generated Images** — arXiv:2606.00872 (ICML 2026, Spotlight) | Adapts to a **new generator with a small labelled context set instead of retraining**: up to **+8.2% over LATTE** |

> ⚠️ **Verified hole:** a targeted search for 2025–2026 arXiv work on **geotagged photo verification / GPS-spoof detection for citizen field reporting** found **nothing directly on point.** The closest are FLiD (identity-document forensics) and the general IML literature. **This means geotag authenticity must be solved cryptographically (device-signed capture attestation), not with ML.** See Gap 6 in Part D.

---

## B11. Privacy

| Paper | Contribution | Key result |
|---|---|---|
| **Practitioners' Perspectives on a Differential Privacy Deployment Registry** — arXiv:2509.13509 | Hierarchical schema + interactive registry **populated with 21 real-world DP deployments**; n=16 practitioner study | Best available inventory of what people actually did |
| **Setting ε is not the Issue in Differential Privacy** — arXiv:2511.06305 (NeurIPS 2025 Position) | Argues the "unintuitive ε" objection is used to justify **unsafe alternatives** |
| ⚠️ **Beyond Theoretical Bounds: Empirical Privacy Loss Calibration (TeDA)** — arXiv:2603.22968 | **The same nominal ε implies very different actual distinguishability across mechanisms** — nominal ε is not comparable across systems |
| **Ball Differential Privacy** — arXiv:2607.04209 | ε-δ indistinguishability restricted to a ball of radius r + **Ball-ReRo reconstruction-robustness certificates**, audited against optimal finite-prior MAP reconstruction attack |
| ⭐⚠️ **INO-SGD: Utility Imbalance under Individualized DP** — arXiv:2605.07930 (ICLR 2026) | **Highly relevant to welfare data:** owners of *more sensitive* data (stigmatized categories) set stronger privacy requirements and end up **severely underrepresented in the model, harming exactly the people they are** |
| **LaDP: Local Layer-wise DP in Federated Learning** — arXiv:2601.01737 | **−46.14% noise injection** vs SOTA while **+102.99% accuracy**; raises reconstruction FID **>12.84%** |
| **Privacy-Preserving FL via DP and HE for CVD Risk** — arXiv:2604.27598 | Real **nationwide Swedish healthcare data**; FL+HE ≈ centralized ML with cryptographic overhead |
| **FedCVR: Recovering Clinical Utility Under DP** — arXiv:2607.19403 | **F1 79.2%, AUC 0.96 at ε ≈ 4.2**; server-side adaptive optimization acts as a **temporal denoiser** for DP noise |
| ⭐ **CE-FedGNN: Communication-Efficient Privacy-Preserving Federated GNNs** — arXiv:2605.26243 | **The right shape for cross-department fraud graphs.** No raw data or per-round embeddings shared; **metric-DP** rather than worst-case DP. O(1/√T) convergence with O(T^{3/4}) communication; validated on **synthetic interbank AML benchmarks** |
| **FedGraph-VASP** — arXiv:2601.17935 | Boundary-embedding exchange + post-quantum Kyber-512/AES-256-GCM. Elliptic Bitcoin **F1 0.508 vs FedSage+ 0.453 (+12.1%)**. **Honest privacy audit: embeddings only partially invertible (R² = 0.32)** |

> ⚠️ **Verified hole:** targeted searches for 2025–2026 work on **k-anonymity applied to beneficiary/welfare registers** and **PPRL for social-protection data** found **nothing on point.** Existing k-anonymity literature is mature but pre-2023 and largely in database venues.

---

# PART C — FEASIBLE TODAY vs STILL RESEARCH

This section is the backbone of the *Feasibility & Implementation Readiness* rubric line. **Knowing your own limits scores higher than overclaiming.**

## ✅ Feasible today, at production quality

| # | Capability | Evidence |
|---|---|---|
| 1 | **Graph-based collusion and shell-company detection on tender data** | GATs transfer cross-market at **84–91%** (2507.12369); PU learning handles the no-confirmed-negatives problem (2512.19491); network features consistently beat red flags alone |
| 2 | **Unsupervised post-award payment anomaly detection with no labels at all** | PHI (2605.12547). Lowest-hanging fruit; works on ordinary payment ledgers |
| 3 | **MT across all 22 scheduled Indian languages** | IndicTrans2 — open, permissively licensed, complete coverage (2305.16307) |
| 4 | **OCR + document parsing for typed/printed docs, including tables** | olmOCR at **$176/million pages** (2502.18443) |
| 5 | **Change detection for large, spectrally distinct assets** — roads, ponds, land levelling, building clusters | **F1 0.83–0.95** on standard benchmarks, including **fully unsupervised** (2606.10775) and **open-vocabulary training-free** (2604.11231) |
| 6 | **Entity matching on clean structured records** | Ditto **F1 ~96%** (2004.00584) |
| 7 | **GraphRAG over a curated entity graph with provenance and citations** | Swiss commercial-registry system (2605.18770) proves the architecture at national registry scale |
| 8 | **On-device inference of 1–4B models on a mid-range Android phone for narrow tasks** | Phi-4-Mini tops OpenASR with a 460M speech LoRA (2503.01743); prompt compression on a Huawei Nova with 95.7% energy reduction (2606.20571) |
| 9 | **Federated learning + DP across departments** | **ε≈4, F1 ~0.79** on real multi-institution health data (2607.19403); federated GNNs with formal metric-DP validated on interbank AML graphs (2605.26243) |
| 10 | **Tamper detection on uploaded identity/bill photos** | Field-localized forensics **AUC 0.88–0.95 with 191K params** (2605.09089) |
| 11 | **Perceptual-hash duplicate image detection** | Not a research problem at all. Standard library code. **This is what CAG did by hand.** |

## ⚠️ Feasible today, with honest quantified degradation

| # | Capability | The real numbers | Design response |
|---|---|---|---|
| 12 | **ASR in Indian languages, noisy rural audio** | Hindi best-case **WER 16.2%**; **Odia best-case 35.1%, only with diarization** (2602.03868). WER **rises with inter-district distance** (2606.09345). **21% of model-language pairs silently emit the wrong script** — invisible to WER (2604.08786) | **No free-form dictation.** Structured slot-filling + verbal confirmation loops + DTMF fallback + script-aware prompting |
| 13 | **OCR on real Indian scanned documents** | Clean synthetic Devanagari: all systems chrF++ 91–98. **300 real printed scans: nine of ten collapse. GPT-5.5 → 58.5 (ties classical EasyOCR). olmOCR-7B → 40.5.** Survivors: Gemini 2.5 Flash 86.3, Claude Opus 4.7 82.2, **open Qwen3-VL-8B 75.2** (2606.29213). Errors concentrate in **conjuncts, matras, nukta** — the marks that distinguish names | Never auto-accept an OCR'd name. Human-in-the-loop for anything evidentiary (MADP 2605.17159 gets 97% automation *with* HITL) |
| 14 | **Handwritten muster rolls** | Isolated Devanagari *characters* are **solved (99.73%, saturated)** (2607.13689). Handwritten **names/addresses are not: CER 29.6%** (2606.05018). **But writer retrieval works at mAP 50.6%** | **Don't try to read the names. Detect that one hand wrote forty rows.** Higher-value signal, achievable accuracy |
| 15 | **LLM-generated SQL over a spending database** | Best proprietary **67–70% EX**; best open-source **58.1%** (2607.06229). On a provenance-aware graph: strong commercial **54–69%**, 7B open **6–19%**, and **the open model never abstains** (2607.25243) | **Do not do this.** Intent → parameterised template router |
| 16 | **Verifying that a generated query is correct** | Best single black-box signal **0.675 AUROC**; two-provider judge ensemble **0.82 AUROC, ECE 0.03**, but honest operating point is **answering 27% of questions at 24% selective risk** (2607.06799). Fine-tuned verifiers **do not transfer** (0.79 → 0.66) | Reinforces #15 |
| 17 | **Satellite verification of *built* assets** | Prithvi-EO-2.0 across 19 real events: **IoU 52% cropland, IoU ≈ 4% built-up** (2606.07780). All GFMs lose **15–20% OOD** (2605.29330). **39% of GFM papers release no weights; 46 documented ≥10-point contradictions** (2605.12678) | **Trust satellite for roads/ponds/land. Treat as weak for houses. Never dispositive.** Always a *trigger for human verification*, never a verdict |
| 18 | **Structured output from on-device SLMs** | Hard JSON schema: validity **61.5% → 100%**, accuracy **19.7% → 11.0%**, wrong-but-valid **49.5% → 88.9%** (2605.26128). Production Android conclusion: **"the most reliable on-device LLM feature is one where the LLM does the least"** (2604.24636) | Reason free, constrain late. Keep the SLM's job tiny |

## ❌ Still research — do not promise these

| # | Capability | Why not |
|---|---|---|
| 19 | **Detecting AI-generated / manipulated photographic evidence in the wild** | GPT-5.1 achieves **48.80%** on a holistic forensic benchmark; expert detectors localize at **IoU 30.09%**; **11 of 25 generators drop average forensic accuracy below 50%** (2604.28177). **Detection is losing the arms race** |
| 20 | **Geotagged photo authenticity / GPS-spoof resistance** | **No credible 2025–26 literature found.** This is a **cryptographic attestation problem (device-signed capture), not an ML problem** |
| 21 | **Privacy-preserving record linkage across welfare registers** | Mature pre-2023 crypto literature, nothing recent addressing Indic name variation. **PPRL + transliteration is unsolved** |
| 22 | **k-anonymity guarantees on beneficiary micro-data** | No recent work; and INO-SGD (2605.07930) shows a serious equity trap — **the most privacy-sensitive subgroups get systematically under-represented** |
| 23 | **Sybil-resistant open citizen-reporting reputation** | **Proved impossibility** for balance-derived voting power (2605.18990: **1,172×–4,039× amplification even under quadratic voting**) and **proved impossibility** for exact-Shapley-fair false-name-proof attribution (2605.07663). The only working answers require **an external identity anchor** (DARTIC 2605.18146) |
| 24 | **A fully autonomous, end-to-end "AI auditor"** | FinRule-Bench: LLMs handle isolated rule verification but **degrade sharply on multi-violation diagnosis** (2603.11339). Evaluator LLMs miss **>50%** of injected quality drops (2406.13439). Financial ML pipelines are **not even deterministic across re-runs** (2605.23955) — fatal if a flag can be legally contested |

---

# PART D — THE GAP ANALYSIS (where the idea comes from)

Two independent research streams — one on Indian government data, one on the academic literature — were run without knowledge of each other. **They converged on the same holes.** That convergence is the strongest signal available that the resulting idea is genuinely novel rather than merely unfamiliar.

## D1. Gaps found in the Indian system (verified, not speculated)

| # | Gap | Evidence |
|---|---|---|
| **G1** | **The audit-to-recovery loop is undigitised.** No public system links: audit finding → responsible officer → recovery order → amount recovered → case closed | AuditOnline: **62,745 observations, 0 settlement reports, 0 ATRs.** Recovery **<13%** |
| **G2** | **No automated forensics on geo-tagged evidence.** NMMS + AwaasSoft ingest **millions** of geo-tagged photographs. **No perceptual-hash duplicate detection, no EXIF/GPS anomaly screening, no satellite-vs-claim change detection** runs on this corpus | CAG had to open **Google Earth by hand**; caught **identical images reused across construction stages** by manual inspection |
| **G3** | **No cross-scheme entity resolution.** PMAY-G, MGNREGS, PDS, PM-KISAN, NSAP beneficiary lists are not publicly joined — **despite LGD codes being the mandated universal location key since 4 Nov 2016**, covering 255,297 GPs. A citizen cannot ask *"what did my panchayat receive across all schemes this year?"* from one place | LGD mandate + portal fragmentation |
| **G4** | **Procurement red-flag analytics do not exist in India.** **No single-bid rate, no repeat-winner concentration index, no award-vs-estimate variance by procuring entity is published by anyone** | CPPP publishes 97,884 tenders and public bid awards; GeM has moved ₹19.8 lakh crore. The standard World Bank/EU screens are simply never run |
| **G5** | **PFMS is a closed ledger.** The system that actually moves the money is login-gated. **Every leakage analysis in India is forced to work from consumption surveys and MIS scrapes instead of the payment rail** | pfms.nic.in login-gated; dashboard returns nothing extractable |
| **G6** | **CAG and CVC findings are trapped in PDFs.** Decades of audit paragraphs — each containing a scheme, a district, an amount and an irregularity type — with **no tagging, no database, no API** | An LLM-based extraction layer turning CAG paragraphs into a queryable observations table **does not exist** |
| **G7** | **No public asset register.** No national machine-readable inventory of panchayat/ULB assets created under public schemes | *"Was this asset actually built, and does it still exist?"* cannot be asked systematically |
| **G8** | **Grievance data is a dashboard, not a dataset.** No API, no grievance-text corpus | DARPG's own review meetings identified only **52 systemic issues** from **4.2 million grievances** |
| **G9** | **Voice is missing.** Every transparency channel — Meri Panchayat, CPGRAMS, eGramSwaraj, AuditOnline — is app-or-web-first | **51.6% of rural women 15+ do not own a phone; 49.1% cannot send a file attachment.** Bhashini is deployed for *translation* but not for *voice-first access* |
| **G10** | **Social audit coverage is thin and shrinking** | Statutorily universal; in 2025-26 only **38.58%** of panchayats covered — and that partial coverage still found **61,347 cases** |

## D2. Gaps found in the academic literature (searched pairwise and multi-way, nothing found)

| # | Novelty gap | What exists separately | What does not exist |
|---|---|---|---|
| ⭐ **N1** | **Procurement collusion graphs + satellite asset verification, jointly** | Collusion detection on bid/contract/ownership data (2507.12369, 2512.19491, 2306.10857). Satellite verification on pixels (2606.07780, 2606.10775) | **No paper closes the loop:** use a graph model to predict which contracts are high-risk, then use bi-temporal change detection to test whether the physical asset those contracts paid for actually appeared. Nearest neighbours: the Mexico paper (network + sanctions, **no imagery**); crop-reference cleaning (2607.23908, imagery embeddings find bad *records* — but for **crop labels, not government assets**). **The strongest genuinely novel combination available** |
| ⭐ **N2** | **Citizen reports as a *supervision signal* for a fraud graph** | Crowdsourcing integrity treats reports as the **end product** (2605.18146, 2606.28062, 2607.24117). Graph fraud detection treats labels as **exogenous** | **Nothing published uses verified citizen reports as weak/PU labels to retrain a procurement or beneficiary graph model** — which is exactly what would break the **"no confirmed positives" bottleneck identified in 2512.19491**. Related but different: Clue2Group (2606.26189) assumes a **professional analyst**, not a villager |
| **N3** | **Indic-language, voice-first interface onto a government spending knowledge graph** | Indic RAG (2506.01615, text, Wikipedia-derived). Indic AudioLLM benchmarking (2606.19157). Auditable GraphRAG over registries (2605.18770, **German/French/Italian**). Provenance-aware NL→query (2607.25243, **English**) | **No paper puts an Indic-language voice query on top of a structured public-spending entity graph with provenance-carrying answers.** Component evidence says it's hard: **16–35% WER × 54–69% NL→query accuracy compound multiplicatively** |
| **N4** | **Entity resolution for Indic transliterated names in a fraud/ghost-beneficiary setting** | Aksharantar: 26M Indic transliteration pairs (2205.03018). Ditto (2004.00584). OT character alignment (1907.10165). d-blink Bayesian ER at census scale (1909.06039) | **Nobody has combined them.** There is **no published Indian-name entity resolution benchmark**, and no work on ghost-beneficiary detection as an ER problem — **despite "same person under three spellings" and "same contractor under four registrations" being the two central fraud mechanisms** |
| **N5** | **Provenance-aware, citizen-contestable explanations** | Ex-GraphRAG shows message-passing encoders **cannot be faithfully audited** (2605.21994). Trajectory-level citation faithfulness (2605.15109). Non-determinism across re-runs (2605.23955) | **No published system produces an explanation that a non-expert citizen can act on and that a government can be legally held to** |
| **N6** | **Sybil-resistant citizen reporting under India's actual identity constraints** | DARTIC achieves anonymity + Sybil resistance **only** by binding pseudonyms to a single access token via zkSNARKs (2605.18146). DAO impossibility proves nothing weaker works (2605.18990) | **Nobody has studied what happens when the identity anchor is a national ID that people are politically reluctant to attach to a corruption complaint.** The central socio-technical unsolved problem, with zero literature |
| ⭐ **N7** | **Muster-roll / attendance-register fraud as writer retrieval** | The Swiss signature-list paper shows OCR fails on handwritten names (**CER 29.6%**) **but writer retrieval works (mAP 50.6%)** for duplicate-submission detection (2606.05018) | **No one has applied writer retrieval to muster rolls, NREGA attendance registers, or ration distribution registers** — where *"one supervisor forged 40 signatures"* is a known, common fraud. **A small, cheap, high-signal, publishable gap** |
| **N8** | **On-device Indic SLM agent with policy-constrained structured output** | Constraint tax (2605.26128), on-device production lessons (2604.24636), Vietnamese SLM test-time scaling (2604.17794) | **None are Indic**, and none combine on-device structured extraction with **column-level access control** (2607.12341). Likely to fail badly on current evidence |
| **N9** | **Cross-department federated fraud graph under Indian data-protection law** | CE-FedGNN (2605.26243), FedGraph-VASP (2601.17935) do federated graph learning for AML with formal privacy | **Neither has been applied to government departments; neither addresses the DPDP Act 2023.** The individualized-DP equity trap (2605.07930) has **never been studied in a welfare context** |
| ⭐ **N10** | **Post-award payment anomalies + graph collusion + document evidence, as one pipeline** | PHI does payments (2605.12547). GAT/PU does tenders (2507.12369, 2512.19491). MADP does documents with HITL (2605.17159). Auditable fraud investigation sketches the agentic wrapper (2607.19266) | **No published system fuses tender-stage graph risk, post-award payment structure, and extracted document evidence (bills, UCs, muster rolls) into a single case file.** Each component is 2025–2026 SOTA; **the fusion is unpublished** |

## D3. The convergence

Lay the two lists side by side:

| Indian gap | Academic gap | The thing that doesn't exist |
|---|---|---|
| G2: millions of unexamined geo-tagged photos; CAG used Google Earth by hand | N1: nobody joins collusion graphs to satellite verification | **A system that predicts which works are high-risk *and then looks at whether they exist*** |
| G1: 62,745 observations, 0 ATRs | N5: no citizen-contestable explanation | **A case file with a clock on it** |
| G10: audits cover 38.58% and still find 61,347 cases | N2: nobody uses citizen reports as training labels | **The citizen as the missing sensor *and* the missing label** |
| G9: no inbound voice channel anywhere in Indian GovTech | N3: no Indic voice onto a spending graph | **A phone number you can call to ask what your panchayat was paid** |
| G3: no cross-scheme entity resolution despite a mandated join key | N4: no Indic-name ER, no ghost-beneficiary ER benchmark | **Ghost detection as a calibrated-uncertainty ER problem** |
| G4: India publishes no single-bid rate | N10: no fused tender + payment + document pipeline | **India's first procurement red-flag table** |

**That table is the idea.** It is written up in `idea.md`.

---

# PART E — RELIABILITY NOTES

## E1. Fully verified — primary source read directly ✅

DBT Bharat estimated-gains table · CPGRAMS PIB parliamentary answer · CPGRAMS live dashboard · MoSPI CMS:T telecom survey via PIB · LGD statistics · **AuditOnline dashboard (the 0 ATRs figure)** · IMPDS portal · GeM and CPPP counters · API Setu counters · Ideas for India PDS leakage tables · CVC annual-report index · eGramSwaraj portal · all Sentinel-2/Landsat sensor specifications · all arXiv IDs listed in Part B (title-verified via arXiv API on 29 July 2026)

## E2. Verified via reputable journalism reporting a primary document 📰

All CAG findings (JJM Maharashtra, MGNREGA Karnataka, PM-POSHAN Odisha) · MGNREGA social audit detection/recovery figures · SNS RTI report card · TI GCB Asia India figures · LibTech wage-delay percentages

**Cite these with attribution to the reporting outlet**, e.g. *"CAG performance audit as reported by Deccan Herald, March 2026."*

## E3. Explicitly NOT verified — ⚠️ do not cite without opening the source

- CMS India Corruption Study 2018 **service-wise** bribery breakdown (land records / police / municipal / PDS / electricity) — PDF unretrievable
- Karnataka ₹6,725.65 cr completed vs ₹5,361.02 cr incomplete works split
- CVC 2024 report internal statistics (200 prosecution sanctions; 7,000 pending court cases)
- ICRIER ₹69,108 crore PDS figure (PDF unretrievable; taken from ET reporting)
- Aadhaar exclusion-error percentages (papers identified, not read)
- The HP / CCI ₹142 crore fine
- **Any English-proficiency percentage for India**
- **Any CPGRAMS satisfaction or reopen rate**
- Any JanMANREGA or Meri Panchayat adoption figure
- Any PMAY-G, PMGSY or Swachh Bharat CAG figure
- Maharashtra "92 lakh bogus Ladki Bahin beneficiaries"
- arXiv IDs for **PC-GNN, GAGA, LayoutLMv3, Donut, Nougat, DocLayout** — real systems, IDs unverified, deliberately omitted
- **Sarvam AI** and **Gemma 3n** have **no arXiv papers** — do not fabricate IDs

## E4. Practical warnings for the build

1. **`mnregaweb4.nic.in` returns "URL Tampered" on direct deep-links.** Budget real engineering time for session-aware crawling of NREGASoft. It holds the best data and is the least link-friendly.
2. **`data.gov.in`'s old `/ogpl_apis` path now 404s.** Use the current portal / RSS.
3. **`cag.gov.in` report pages can return XML parse errors.** Fetch the PDFs from the index rather than the detail pages.
4. **Quote the pessimistic number.** Wherever the literature offers an in-distribution and an out-of-distribution figure, the OOD figure is the one that will survive a technical judge's question.
5. **The MIT-license requirement is a design constraint, not a footnote.** Every core dependency must be openly licensed: IndicTrans2 (open weights, permissive), Prithvi-EO-2.0 (HuggingFace/TerraTorch), TerraMind (fully open-sourced, permissive), PaddleOCR 3.0 (Apache-2.0), Qwen3-VL-8B (open, one 24 GB GPU), Sentinel-2 (free), LGD (bulk download).

---

*End of RESEARCH.md — the idea built on this evidence is in `idea.md`; the implementation is in `PLAN.md`.*
