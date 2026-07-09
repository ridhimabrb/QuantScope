"""
Discounted cash flow bond valuation, duration, and modified duration.

This is real, deterministic finance math (not ML) -- it matches the
"Bond Pricing Calculator" / "Present Value Analysis" features described
in the ML-Powered-Bond-Yield-Forecaster README, plus the "Duration" and
"Modified Duration" items listed there under Future Enhancements.
"""

from dataclasses import dataclass


@dataclass
class BondResult:
    price: float
    macaulay_duration: float
    modified_duration: float


def price_bond(face_value: float, coupon_rate_pct: float, years_to_maturity: float,
               market_yield_pct: float, frequency: int = 2) -> BondResult:
    """
    face_value: e.g. 1000
    coupon_rate_pct: annual coupon rate, e.g. 7.2 for 7.2%
    years_to_maturity: e.g. 10
    market_yield_pct: annual market yield / YTM, e.g. 7.0 for 7.0%
    frequency: coupons per year (2 = semi-annual, 1 = annual)
    """
    n_periods = int(round(years_to_maturity * frequency))
    coupon_per_period = (coupon_rate_pct / 100) * face_value / frequency
    y_per_period = (market_yield_pct / 100) / frequency

    price = 0.0
    weighted_time = 0.0
    for t in range(1, n_periods + 1):
        cash_flow = coupon_per_period + (face_value if t == n_periods else 0)
        discount_factor = (1 + y_per_period) ** (-t)
        pv = cash_flow * discount_factor
        price += pv
        weighted_time += (t / frequency) * pv

    macaulay = weighted_time / price if price else 0.0
    modified = macaulay / (1 + y_per_period) if price else 0.0

    return BondResult(price=price, macaulay_duration=macaulay, modified_duration=modified)


def reprice_under_shock(face_value: float, coupon_rate_pct: float, years_to_maturity: float,
                         market_yield_pct: float, shock_bps: float, frequency: int = 2) -> BondResult:
    """Reprices the bond after a parallel yield shock, given in basis points."""
    shocked_yield = market_yield_pct + shock_bps / 100
    return price_bond(face_value, coupon_rate_pct, years_to_maturity, shocked_yield, frequency)
