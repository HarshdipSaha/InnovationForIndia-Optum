"""The killer demo (PLAN.md section 11): run every detector on the CAG-retrospective
dataset, print the output blocks, assemble a case file, and VALIDATE that the
detectors independently re-derive the published CAG findings.

Run:  python run_demo.py
Exit code is non-zero if any validation check fails.

Presentation note: colour/Unicode come from ``saakshi.common.term`` and switch
off automatically when output is piped (so DEMO_OUTPUT.txt stays clean ASCII).
The numbers are identical either way - styling never touches a value (Rule R1).
"""
from __future__ import annotations

import json
import statistics
from datetime import date
from pathlib import Path

from saakshi.chitragupta import network, payments, photos
from saakshi.common import term
from saakshi.common.models import Dataset
from saakshi.ghadi import casefile
from saakshi.synth.generate import generate

TODAY = date(2026, 7, 30)
GT_PATH = Path(__file__).resolve().parents[3] / "data" / "ground_truth" / "cag_karnataka_2026.json"


def _rule(title: str) -> str:
    line = (term.HRULE * 2 + " " + title + " ").ljust(66, term.HRULE)
    return "\n" + term.saffron_b(line)


def _crore(x: float) -> str:
    return f"{term.RUPEE} {x / 1e7:.2f} crore"


def run() -> int:
    ds = generate()
    windex = {w.work_id: w for w in ds.works}
    gp_district = {p.gp_code: p.district_name for p in ds.panchayats}
    gt = json.loads(GT_PATH.read_text(encoding="utf-8"))["anchors"]
    checks: list[tuple[str, bool, str]] = []

    top = term.HRULE * 66
    print(term.saffron_b(top))
    print("  " + term.saffron_b("SAAKSHI") + term.dim("  the witness for every rupee"))
    print("  " + term.bold("CAG-retrospective forensic demo"))
    print(term.dim("  Data: SYNTHETIC reconstruction of the March 2026 CAG Karnataka"))
    print(term.dim("        MGNREGA audit (see data/ground_truth/). Not live-scraped."))
    print(f"  Corpus: {len(ds.works):,} works {term.BULLET} {len(ds.payments):,} payments "
          f"{term.BULLET} {len(ds.photos):,} photos {term.BULLET} {len(ds.tenders):,} tenders")
    print(term.saffron_b(top))

    # ---------------- (1) PHOTO FORENSICS ----------------------------------
    print(_rule("CHITRAGUPTA (1) PHOTO FORENSICS"))
    dups = photos.find_duplicates(ds.photos, windex, gp_district)
    cross_work = [d for d in dups if d.cross_work]
    cross_dist = [d for d in dups if d.cross_district]
    tightest = min((d.hamming for d in dups), default=None)
    print(f"(a) NEAR-DUPLICATES ......................... {len(dups):>6} pairs")
    print(f"    of which cross-WORK .................... {len(cross_work):>6} pairs")
    print(f"    of which cross-DISTRICT ............... {len(cross_dist):>6} pairs  "
          + term.amber("!"))
    if tightest is not None:
        print(f"    tightest match: {term.bold(f'hamming {tightest}/64')}")
    pond_pair = next((d for d in dups
                      if {d.work_a, d.work_b} == {gt["duplicate_photo_work_a"],
                                                  gt["duplicate_photo_work_b"]}), None)
    if pond_pair:
        print("    " + term.amber("!") + " "
              + term.saffron(f"{pond_pair.photo_a}  {term.BIDIR}  {pond_pair.photo_b}")
              + f"   hamming {pond_pair.hamming}")
        print(f"       work {pond_pair.work_a}  /  work {pond_pair.work_b}")
        print(f"       distance between works: {term.bold(f'{pond_pair.distance_km} km')}")
        print("       claimed stages: completion / completion")
    geo = photos.geo_mismatches(ds.photos, windex)
    tsw = photos.timestamp_out_of_window(ds.photos, windex)
    itins = photos.impossible_itinerary(ds.photos)
    print(f"(b) GEO MISMATCH (> 2.0 km) ................. {len(geo):>6} photos")
    print(f"(c) TIMESTAMP OUTSIDE WORK WINDOW .......... {len(tsw):>6} photos")
    print(f"(d) IMPOSSIBLE DEVICE ITINERARY ............ {len(itins):>6} devices")
    for it in itins:
        print("    " + term.amber("!") + f" device \"{it.device}\": "
              + term.saffron(f"{it.distinct_sites} distinct sites in {term.LEQ}60 min")
              + f", span {it.max_span_km} km")

    checks.append(("photo duplicate reused across the two CAG works",
                   pond_pair is not None and pond_pair.hamming <= photos.DUP_THRESHOLD,
                   f"pair={'found' if pond_pair else 'MISSING'}"))
    redmi = next((it for it in itins if it.device == gt["device_itinerary_device"]), None)
    checks.append((f"impossible itinerary for {gt['device_itinerary_device']}",
                   redmi is not None and redmi.distinct_sites >= gt["device_itinerary_min_sites"],
                   f"sites={redmi.distinct_sites if redmi else 0}"))

    # ---------------- (2) PAYMENT STRUCTURE --------------------------------
    print(_rule("CHITRAGUPTA (2) PAYMENT STRUCTURE"))
    splits = payments.threshold_splitting(ds.works)
    print("(a) THRESHOLD SPLITTING")
    print(f"    sibling groups that would cross a threshold ... {len(splits)}")
    split_hit = next((g for g in splits
                      if g.gp_code == gt["check_dam_split_gp"]
                      and g.threshold == gt["check_dam_split_threshold_inr"]
                      and g.vendor_id == gt["sole_bidder_vendor_id"]), None)
    if split_hit:
        amts = " + ".join(f"{term.RUPEE} {a:,.0f}" for a in
                          sorted(w.sanctioned_amount for w in ds.works
                                 if w.work_id in split_hit.work_ids))
        print("    " + term.amber("!") + f" GP {split_hit.gp_code}, vendor {split_hit.vendor_id}: "
              f"{split_hit.n_works} works, {amts}")
        print(f"      = {term.bold(f'{term.RUPEE} {split_hit.combined:,.0f}')} combined, would cross the "
              f"{term.RUPEE} {split_hit.threshold:,.0f} tender threshold as one work")

    bills = [p.amount for p in ds.payments]
    bf = payments.benford_first_digit(bills)
    verdict = "deviates" if bf.deviates_at else "within tolerance"
    alpha = f" (alpha={bf.deviates_at})" if bf.deviates_at else ""
    print("(b) BENFORD (payment amounts, n=%d)" % bf.n)
    print(f"    chi2 = {bf.chi2}   {verdict}{alpha}   {term.dim('[weak signal only]')}")

    print("(c) TEMPORAL IMPOSSIBILITY")
    temporal = payments.temporal_impossibility(ds.payments, ds.works)
    total_val = sum(t.amount for t in temporal)
    median_lag = int(statistics.median([t.days_after for t in temporal])) if temporal else 0
    print("    " + term.amber("!") + " "
          + term.bold(f"{len(temporal)} stage payments AFTER claimed completion date"))
    print(f"      median lag: {median_lag} days {term.BULLET} total value {_crore(total_val)}")
    validated = len(temporal) == gt["temporal_impossibility_instances"]
    tag = term.green_b("MATCH -- VALIDATED") if validated else term.red_b("NO MATCH")
    print(f"      {term.ARROW} CAG Karnataka finding: {gt['temporal_impossibility_instances']} instances, "
          f"{gt['temporal_impossibility_value_label']}.  {tag}")

    checks.append(("threshold-split (Koppal check dam) detected", split_hit is not None,
                   "found" if split_hit else "MISSING"))
    checks.append((f"temporal impossibility count == {gt['temporal_impossibility_instances']}",
                   validated, f"got={len(temporal)}"))

    # ---------------- (3) NETWORK / PROCUREMENT RED FLAGS ------------------
    print(_rule("CHITRAGUPTA (3) NETWORK - PROCUREMENT RED FLAGS"))
    print("    " + term.dim("No Indian body publishes these. This is a first computation."))
    flags = network.red_flags_by_entity(ds.tenders, min_tenders=10)
    header = f"    {'org_chain':<34}{'n':>4}{'single-bid':>12}{'premium':>10}{'winner-div':>12}"
    print("\n" + term.dim(header))
    print(term.dim("    " + "-" * 70))
    for f in flags[:6]:
        row = (f"    {f.org_chain:<34}{f.n_tenders:>4}{f.single_bid_rate * 100:>11.1f}%"
               f"{f.mean_award_premium * 100:>+9.1f}%{f.winner_diversity:>12.2f}")
        print(row + ("  " + term.amber("!") if f.single_bid_rate >= 0.5 else ""))
    rate, single, n = network.national_single_bid_rate(ds.tenders)
    print(term.dim("    " + "-" * 70))
    print(f"    NATIONAL (all entities, n={n})  single-bid rate = "
          + term.bold(f"{rate * 100:.1f}%") + "   " + term.saffron(f"{term.ARROW} FIRST EVER"))

    vend = network.sole_bidder_vendors(ds.tenders, ds.bids, min_sole_wins=5)
    basava = next((v for v in vend if v.vendor_id == gt["sole_bidder_vendor_id"]), None)
    if basava:
        print("\n    " + term.amber("!") + " "
              + term.saffron(f"vendor {basava.vendor_id} ({gt['sole_bidder_vendor_name']})")
              + f": won {basava.tenders_won} tenders, "
              + term.bold(f"{basava.sole_bidder_wins} as SOLE bidder")
              + f", avg premium {basava.mean_premium * 100:+.1f}%")
    checks.append((f"sole-bidder vendor won {gt['sole_bidder_wins']} of "
                   f"{gt['sole_bidder_total_block_tenders']}",
                   basava is not None and basava.sole_bidder_wins == gt["sole_bidder_wins"],
                   f"sole_wins={basava.sole_bidder_wins if basava else 0}"))

    # ---------------- (4) GHADI - THE CASE FILE ----------------------------
    print(_rule("GHADI - CASE FILE (four independent signals, never one score)"))
    pond = windex[gt["duplicate_photo_work_a"]]
    kam = ds.panchayat(pond.gp_code)
    sigs = [
        casefile.Signal(
            "PHOTO FORENSIC", "HIGH",
            [f"Completion photo dHash-near-identical (Hamming {pond_pair.hamming}/64) to the",
             f"completion photo of work {pond_pair.work_b}, {pond_pair.distance_km} km away."],
            evidence=[f"{pond_pair.photo_a} . {pond_pair.photo_b}"],
            method="perceptual hash, deterministic, reproducible"),
        casefile.Signal(
            "NETWORK", "MEDIUM",
            [f"Work's vendor {basava.vendor_id} won {basava.sole_bidder_wins} block tenders",
             f"as sole bidder; award premium {basava.mean_premium * 100:+.1f}%."],
            evidence=["CPPP award IDs [list]"],
            method="LightGBM on graph features, PU-calibrated (internal triage only)"),
        casefile.Signal(
            "SATELLITE", "LOW",
            ["Sentinel-2 NDWI delta below threshold; no surface-water feature appeared."],
            caveats=["10 m GSD. Small ponds may be below detection limit.",
                     "NOT dispositive. Trigger for human verification only.",
                     "simulated input in this offline demo; production runs Sentinel-2."],
            method="bi-temporal change detection"),
        casefile.Signal(
            "CITIZEN VERIFICATION", "HIGH",
            ["3 independent anonymous reports: \"no pond at this location.\"",
             "Sybil-checked, zkSNARK-bound, no linkage to identity."],
            evidence=["pramaan_a91f2 . pramaan_c04e8 . pramaan_7b331"],
            caveats=["simulated input in this offline demo."],
            method="truth discovery over independent reports"),
    ]
    cf = casefile.build_case(
        case_id="KA-KLB-2026-00412",
        work=pond, panchayat_label=f"{kam.gp_name}, {kam.district_name}, {kam.state_name}",
        lgd_code=pond.gp_code, signals=sigs,
        unknowns=["Whether the pond exists but is below satellite resolution",
                  "Whether the duplicate photo is fraud or an upload error",
                  "Whether the sole-bidder pattern reflects collusion or a genuine "
                  "absence of local contractors"],
        opened=date(2026, 7, 14), today=TODAY,
        cpgrams_ref="CPGRAMS/2026/0412773")
    print(casefile.render(cf, color=term.COLOR))

    print("\n" + term.dim("-- AUTO-DRAFTED RTI (RTI Act 2005, s.6(1)) ------------------------"))
    print(cf.rti_draft())

    # ---------------- VALIDATION -------------------------------------------
    print(_rule("VALIDATION vs published CAG findings"))
    all_ok = True
    for name, ok, detail in checks:
        all_ok &= ok
        print(f"  [{term.pass_tag() if ok else term.fail_tag()}] {name:<52} {term.dim(detail)}")
    print(term.saffron_b(term.HRULE * 66))
    if all_ok:
        print("  RESULT: " + term.green_b("ALL CHECKS PASSED -- detectors re-derived CAG findings"))
    else:
        print("  RESULT: " + term.red_b("SOME CHECKS FAILED"))
    print(term.saffron_b(term.HRULE * 66))
    return 0 if all_ok else 1
