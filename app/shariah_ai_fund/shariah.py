from __future__ import annotations

from dataclasses import dataclass

from .models import Asset, ComplianceResult


@dataclass(frozen=True)
class ShariahPolicy:
    max_debt_ratio: float = 0.33
    max_interest_income_ratio: float = 0.05
    prohibited_sectors: tuple[str, ...] = (
        "conventional_banking",
        "gambling",
        "alcohol",
        "tobacco",
        "weapons",
        "adult_entertainment",
    )


class ShariahComplianceEngine:
    def __init__(self, policy: ShariahPolicy | None = None):
        self.policy = policy or ShariahPolicy()

    def evaluate(self, asset: Asset) -> ComplianceResult:
        reasons: list[str] = []

        sector_ok = asset.sector.lower() not in self.policy.prohibited_sectors
        debt_ok = asset.debt_ratio <= self.policy.max_debt_ratio
        interest_ok = (
            asset.interest_income_ratio <= self.policy.max_interest_income_ratio
        )

        if not sector_ok:
            reasons.append("sector_prohibited")
        if not debt_ok:
            reasons.append("debt_ratio_exceeded")
        if not interest_ok:
            reasons.append("interest_income_exceeded")

        score = 1.0
        if not sector_ok:
            score -= 0.5
        if not debt_ok:
            score -= 0.3
        if not interest_ok:
            score -= 0.2

        return ComplianceResult(
            symbol=asset.symbol,
            compliant=(sector_ok and debt_ok and interest_ok),
            score=max(0.0, round(score, 3)),
            reasons=tuple(reasons),
        )
