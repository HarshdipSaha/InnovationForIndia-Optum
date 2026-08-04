"""Detector tests. Runnable with either:

    python -m unittest discover -s tests      (zero dependencies)
    pytest                                    (if installed)

Each test asserts that a detector re-derives a specific published CAG finding
from the synthetic reconstruction, plus the safety properties (determinism, no
fused score).
"""
import json
import unittest
from pathlib import Path

import tests.conftest_path  # noqa: F401  (side effect: puts src/ on sys.path)

from saakshi.chitragupta import network, payments, photos  # noqa: E402
from saakshi.ghadi import casefile  # noqa: E402
from saakshi.synth.generate import generate  # noqa: E402

GT = json.loads((Path(__file__).resolve().parents[1]
                 / "data" / "ground_truth" / "cag_karnataka_2026.json")
                .read_text(encoding="utf-8"))["anchors"]


class DetectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = generate()
        cls.windex = {w.work_id: w for w in cls.ds.works}
        cls.gp_district = {p.gp_code: p.district_name for p in cls.ds.panchayats}

    # ---- determinism (Rule R1) --------------------------------------------
    def test_dhash_is_deterministic(self):
        g = [[i * 7 % 256 for i in range(9)] for _ in range(8)]
        self.assertEqual(photos.dhash(g), photos.dhash([row[:] for row in g]))
        self.assertEqual(photos.dhash(g).bit_length() <= 64, True)

    def test_generate_is_deterministic(self):
        a, b = generate(), generate()
        self.assertEqual(len(a.works), len(b.works))
        self.assertEqual([w.work_id for w in a.works], [w.work_id for w in b.works])

    # ---- (1) photo forensics ----------------------------------------------
    def test_reused_completion_photo_detected(self):
        dups = photos.find_duplicates(self.ds.photos, self.windex, self.gp_district)
        pair = next((d for d in dups
                     if {d.work_a, d.work_b} == {GT["duplicate_photo_work_a"],
                                                 GT["duplicate_photo_work_b"]}), None)
        self.assertIsNotNone(pair, "the reused completion photo was not detected")
        self.assertLessEqual(pair.hamming, photos.DUP_THRESHOLD)
        self.assertTrue(pair.cross_district)
        self.assertGreater(pair.distance_km, 50)

    def test_impossible_itinerary_detected(self):
        flags = photos.impossible_itinerary(self.ds.photos)
        f = next((x for x in flags if x.device == GT["device_itinerary_device"]), None)
        self.assertIsNotNone(f)
        self.assertGreaterEqual(f.distinct_sites, GT["device_itinerary_min_sites"])

    # ---- (2) payment forensics --------------------------------------------
    def test_temporal_impossibility_matches_cag_462(self):
        flags = payments.temporal_impossibility(self.ds.payments, self.ds.works)
        self.assertEqual(len(flags), GT["temporal_impossibility_instances"])

    def test_threshold_split_detected(self):
        splits = payments.threshold_splitting(self.ds.works)
        hit = next((g for g in splits
                    if g.gp_code == GT["check_dam_split_gp"]
                    and g.vendor_id == GT["sole_bidder_vendor_id"]
                    and g.threshold == GT["check_dam_split_threshold_inr"]), None)
        self.assertIsNotNone(hit)
        self.assertGreaterEqual(hit.combined, GT["check_dam_split_threshold_inr"])

    def test_benford_returns_structured_result(self):
        r = payments.benford_first_digit([p.amount for p in self.ds.payments])
        self.assertEqual(sum(r.observed), r.n)
        self.assertEqual(len(r.observed), 9)

    # ---- (3) network -------------------------------------------------------
    def test_single_bid_rate_computable(self):
        rate, single, n = network.national_single_bid_rate(self.ds.tenders)
        self.assertGreater(n, 0)
        self.assertTrue(0.0 <= rate <= 1.0)

    def test_sole_bidder_vendor_flagged(self):
        vend = network.sole_bidder_vendors(self.ds.tenders, self.ds.bids)
        v = next((x for x in vend if x.vendor_id == GT["sole_bidder_vendor_id"]), None)
        self.assertIsNotNone(v)
        self.assertEqual(v.sole_bidder_wins, GT["sole_bidder_wins"])

    # ---- (4) case file: no fused score, carries uncertainty ---------------
    def test_case_file_never_fuses_a_single_score(self):
        pond = self.windex[GT["duplicate_photo_work_a"]]
        cf = casefile.build_case(
            case_id="T1", work=pond, panchayat_label="X", lgd_code=pond.gp_code,
            signals=[casefile.Signal("PHOTO FORENSIC", "HIGH", ["x"]),
                     casefile.Signal("NETWORK", "MEDIUM", ["y"])],
            unknowns=["z"], opened=pond.sanction_date, today=pond.sanction_date)
        text = casefile.render(cf)
        self.assertIn("WHAT WE DO NOT KNOW", text)
        self.assertIn("QUESTION, not a verdict", text)
        # there must be no single composite "corruption score" anywhere
        self.assertNotIn("corruption score", text.lower())
        self.assertNotIn("risk: 0.", text.lower())


if __name__ == "__main__":
    unittest.main()
