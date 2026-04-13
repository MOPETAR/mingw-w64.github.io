from __future__ import annotations

from .models import Asset, ComplianceResult


def risk_adjusted_signal(asset: Asset) -> float:
    risk_floor = max(asset.risk, 1e-6)
    return max(asset.expected_return / risk_floor, 0.0)


def allocate_portfolio(
    assets: list[Asset],
    compliance_map: dict[str, ComplianceResult],
    max_single_weight: float = 0.4,
) -> dict[str, float]:
    eligible_assets = [
        asset for asset in assets if compliance_map.get(asset.symbol) and compliance_map[asset.symbol].compliant
    ]

    if not eligible_assets:
        return {}

    raw_scores = {asset.symbol: risk_adjusted_signal(asset) for asset in eligible_assets}
    total = sum(raw_scores.values())
    if total <= 0:
        equal = 1.0 / len(eligible_assets)
        return {asset.symbol: round(min(equal, max_single_weight), 4) for asset in eligible_assets}

    weights = {symbol: score / total for symbol, score in raw_scores.items()}

    # soft cap normalization
    capped = {symbol: min(weight, max_single_weight) for symbol, weight in weights.items()}
    capped_total = sum(capped.values())

    if capped_total == 0:
        return {}

    return {symbol: round(weight / capped_total, 4) for symbol, weight in capped.items()}
