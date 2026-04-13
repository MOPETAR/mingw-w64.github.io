from __future__ import annotations

from .allocation import allocate_portfolio
from .models import Asset
from .shariah import ShariahComplianceEngine


def demo_assets() -> list[Asset]:
    return [
        Asset(
            symbol="TSLA",
            name="Tesla",
            sector="manufacturing",
            debt_ratio=0.24,
            interest_income_ratio=0.01,
            expected_return=0.18,
            risk=0.30,
        ),
        Asset(
            symbol="ABCBANK",
            name="ABC Bank",
            sector="conventional_banking",
            debt_ratio=0.22,
            interest_income_ratio=0.20,
            expected_return=0.11,
            risk=0.15,
        ),
        Asset(
            symbol="SUKUK1",
            name="Sukuk Basket",
            sector="sukuk",
            debt_ratio=0.10,
            interest_income_ratio=0.00,
            expected_return=0.07,
            risk=0.08,
        ),
    ]


def run_phase1_pipeline(assets: list[Asset] | None = None) -> dict[str, object]:
    assets = assets or demo_assets()
    engine = ShariahComplianceEngine()

    compliance_results = {asset.symbol: engine.evaluate(asset) for asset in assets}
    allocation = allocate_portfolio(assets, compliance_results)

    return {
        "compliance": {
            symbol: {
                "compliant": result.compliant,
                "score": result.score,
                "reasons": list(result.reasons),
            }
            for symbol, result in compliance_results.items()
        },
        "allocation": allocation,
    }
