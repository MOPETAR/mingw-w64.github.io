import unittest

from shariah_ai_fund.models import Asset
from shariah_ai_fund.pipeline import run_phase1_pipeline
from shariah_ai_fund.shariah import ShariahComplianceEngine


class ShariahAIFundTests(unittest.TestCase):
    def test_prohibited_sector_is_non_compliant(self):
        engine = ShariahComplianceEngine()
        asset = Asset(
            symbol="BANKX",
            name="Bank X",
            sector="conventional_banking",
            debt_ratio=0.2,
            interest_income_ratio=0.01,
            expected_return=0.1,
            risk=0.2,
        )
        result = engine.evaluate(asset)
        self.assertFalse(result.compliant)
        self.assertIn("sector_prohibited", result.reasons)

    def test_phase1_pipeline_returns_allocation_for_compliant_assets(self):
        result = run_phase1_pipeline()
        self.assertIn("allocation", result)
        self.assertTrue(result["allocation"])
        self.assertNotIn("ABCBANK", result["allocation"])


if __name__ == "__main__":
    unittest.main()
