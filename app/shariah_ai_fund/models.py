from dataclasses import dataclass


@dataclass(frozen=True)
class Asset:
    symbol: str
    name: str
    sector: str
    debt_ratio: float
    interest_income_ratio: float
    expected_return: float
    risk: float


@dataclass(frozen=True)
class ComplianceResult:
    symbol: str
    compliant: bool
    score: float
    reasons: tuple[str, ...]
