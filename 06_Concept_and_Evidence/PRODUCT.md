# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS/JS (vanilla), no framework and no build step — opens directly via `file://` and deploys as-is to GitHub Pages / Netlify. Offered to the user as the default for a self-contained hackathon deliverable ("no node_modules"); the user accepted. Consistent with the prototype's own "git clone && run, zero dependencies" ethos.

## Users

- **Product users (whom SAAKSHI serves):** rural welfare beneficiaries such as "Lakshmi" — often non-literate or low-literacy, without a personal smartphone (only 48.4% of rural women 15+ own one), and not English/Hindi speakers — who want to know what was spent in their village and can physically verify whether an asset exists. Secondary: state Social Audit Units, RTI activists, journalists, and government officers (Ministry of Panchayati Raj / DARPG) who must act on findings.
- **Audience of THIS website (confirmed with the user):** hackathon **judges/jury** (technical + policy) evaluating the TechGig × Optum submission, plus general public / press. The site is a Persuade surface optimized for the "Presentation & Communication" rubric line; it explains the project, it is not the product UI.

## Product Purpose

A **read-only forensic and accountability layer** over India's existing public government-spending data, plus a toll-free multilingual voice channel, that surfaces evidenced, contestable, time-bound **questions** about welfare spending — and then asks the one citizen who can see the asset to verify it. Success = detection stops being supply-constrained (100% machine-screening vs. 38.58% manual audit) and findings stop going nowhere (against AuditOnline's 62,745 observations and 0 Action Taken Reports).

## Positioning

The mechanism a neighbour could not truthfully copy: the **citizen-verification loop** — a cryptographically anonymous villager's "there is no pond here", corroborated by an independent machine signal, becomes a **Positive-Unlabeled training label** that retrains the fraud model, closing the "no confirmed positives" gap that blocks all procurement-fraud ML. Plus India's-first public computations on already-public data joined on the LGD code (national single-bid rate; audit-finding → recovery tracker; cross-scheme panchayat view).

## Operating Context

Eleven public portals (eGramSwaraj, NREGASoft, CPPP, GeM, AuditOnline, CPGRAMS, DBT Bharat, IMPDS, LGD, data.gov.in, API Setu) joined on the LGD code (mandated universal key since 4 Nov 2016). CAG performance audits; NMMS/AwaasSoft geo-tagged photo corpus; RTI Act 2005 §6(1); MGNREGA §17 social audit / Gram Sabha; Bhashini DPI; DPDP Act 2023. Reference case: Kamalapur GP, Kalaburagi, Karnataka (LGD 226534), work KA-KLB-2026-00412.

## Capabilities and Constraints

Six layers: KOSH (ledger graph) · CHITRAGUPTA (four independent detectors — photo pHash, payment/temporal, network/single-bid, satellite change — **never fused into one score**) · NAAM-MILAN (Indic entity resolution, calibrated posteriors, never a hard verdict) · VAANI (intent-router IVR, **an LLM never writes a query**) · PRAMAAN (zkSNARK-anonymous citizen reports → PU labels) · GHADI (accountability clock: auto-drafted RTI + CPGRAMS, public countdown, recovery ledger). Hard constraints: MIT license; read-only / post-hoc (**never denies a payment, blocks a job card, or gates a ration**); no raw Aadhaar ingested; deterministic citizen-facing path; every honest limit shipped with its capability.

## Brand Commitments

Name **SAAKSHI (साक्षी)** — "the witness". Tagline **"the witness for every rupee."** Naming motif: *Chitragupta* (the divine accountant who records every deed) and *sākṣī* (the witness whose testimony makes a fact admissible). Established visual world to **inherit** from the pitch deck: cream `#F4F0E6`, navy `#202A3E`, saffron `#D98A2B`, forensic green `#2E8B6B`; Georgia/serif display + a workhorse sans; Devanagari script accents (साक्षी · कोष · वाणी · घड़ी); an evidence-dossier / ledger sensibility with the ⚠ honest-limit callout as a first-class element. Theme 05 — GovTech & Public Service Delivery (TechGig × Optum, "Inclusive Innovation for Bharat").

## Evidence on Hand

`idea.md`, `PLAN.md`, `RESEARCH.md` (every headline number carries a ✅ / 📰 / ⚠️ reliability marker), `saakshi/SAAKSHI_Application_Form.md`, the runnable stdlib prototype (`saakshi/run_demo.py` — 10/10 tests, 5/5 validation checks, colorized terminal output in `docs/DEMO_OUTPUT.txt`), the GHADI case file for KA-KLB-2026-00412 with its auto-drafted RTI, and the 18-slide deck (`saakshi/SAAKSHI.pptx`). **Must not be fabricated:** team names/contacts are placeholders; the toll-free number is illustrative; the prototype dataset is a *synthetic reconstruction* of published CAG findings (not live-scraped); the satellite and citizen-verification signals in the offline demo are simulated inputs. No live hosting/deployment exists.

## Product Principles

1. **Ship the honest limit with the capability** — overclaiming loses a technical judge and hurts people.
2. **Read-only and post-hoc** — a false positive costs an official an explanation; it never costs a citizen their rice.
3. **Determinism for anything a citizen sees** — a number that changes on re-run cannot survive a legal challenge.
4. **Reuse digital public infrastructure; do not rebuild it.**
5. **A case file is a question, not a verdict** — four independent signals, an explicit "what we do not know", never one fused score.

## Accessibility & Inclusion

Inclusion is the product's entire thesis (non-literate, non-smartphone, non-English rural users), so the website must itself be exemplary: WCAG 2.1 AA contrast, full keyboard operability, semantic landmarks/headings, visible focus, `prefers-reduced-motion` honored for every animation (including the simulated live-run), and no meaning carried by color alone.
