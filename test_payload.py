import unittest
import json

class TestCrownSovereignPayload(unittest.TestCase):
    def setUp(self):
        self.valid_payload = {
            "@context": "https://schema.org",
            "@type": "CrownSovereignMatrixCodex",
            "enclaveDesignation": "HQ-BASE-01",
            "tier": "Diamond-Tier-1",
            "grade": "Supreme Imperial Crown Estate Standard Grade",
            "centralAxis": "SCION_XP_CHI_RHO",
            "coordinates": {
                "googleMapsNexus": "ChIJP5RO5Cc7yIkR5jhtifTwkmA",
                "goldenNodesCount": 11,
                "driftTolerance": 0.00
            },
            "systemOwner": {
                "name": "Vincent Tyrone Ellis",
                "orcid": "0009-0002-7219-1363",
                "lei": "506700GE1G29325QX363"
            }
        }

    def test_valid_payload(self):
        # Ensure a fully formed payload passes configuration criteria
        self.assertEqual(self.valid_payload["enclaveDesignation"], "HQ-BASE-01")
        self.assertEqual(self.valid_payload["tier"], "Diamond-Tier-1")
        self.assertEqual(self.valid_payload["coordinates"]["goldenNodesCount"], 11)

    def test_malformed_missing_axis(self):
        # Payload must fail if central meridian alignment axis is missing
        malformed = self.valid_payload.copy()
        del malformed["centralAxis"]
        with self.assertRaises(KeyError):
            _ = malformed["centralAxis"]

    def test_invalid_drift_tolerance(self):
        # Strict zero-drift enforcement
        malformed = self.valid_payload.copy()
        malformed["coordinates"]["driftTolerance"] = 0.05
        self.assertTrue(malformed["coordinates"]["driftTolerance"] > 0.00)

if __name__ == "__main__":
    unittest.main()
