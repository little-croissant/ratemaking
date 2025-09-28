"""
Exposure calculation functions for various P&C lines

This module will contain:
- Earned exposure calculations
- Policy term adjustments
- Exposure base conversions
- Territory and class plan exposure allocation

TODO: Implementation coming in future releases
"""


from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


def parse_quarter(quarter_str: str) -> datetime:
    """Parse a string like '2017 Q1' into a datetime object for the first day of the quarter."""
    year, q = quarter_str.split()
    year = int(year)
    q = int(q[1])
    month = 3 * (q - 1) + 1
    return datetime(year, month, 1)


def add_months(dt: datetime, months: int) -> datetime:
    """Add months to a datetime object."""
    year = dt.year + (dt.month + months - 1) // 12
    month = (dt.month + months - 1) % 12 + 1
    return datetime(year, month, 1)


def calculate_policy_year_earned_exposures(exposure_table: List[Dict[str, Any]], policy_year: int, as_of: datetime) -> float:
    """
    Calculate earned exposures for a given policy year as of a specific date.
    Assumes all policies are annual and written at the start of each quarter.
    """
    earned = 0.0
    for row in exposure_table:
        q_date = parse_quarter(row['quarter'])
        if q_date.year == policy_year:
            # Policy written at q_date, annual, so earns over next 12 months
            policy_end = add_months(q_date, 12)
            # Earned as of as_of date is min(as_of, policy_end) - q_date
            months_earned = max(
                0, min((as_of - q_date).days, (policy_end - q_date).days)) / 365.25
            earned += row['written'] * min(months_earned, 1.0)
    return earned


def calculate_in_force_exposures(exposure_table: List[Dict[str, Any]], as_of: datetime) -> float:
    """
    Calculate in-force exposures as of a specific date.
    In-force means policies that are active on that date.
    """
    in_force = 0.0
    for row in exposure_table:
        q_date = parse_quarter(row['quarter'])
        policy_end = add_months(q_date, 12)
        if q_date <= as_of < policy_end:
            in_force += row['written']
    return in_force


def calculate_calendar_year_unearned_exposures(exposure_table: List[Dict[str, Any]], calendar_year: int) -> float:
    """
    Calculate unearned exposures for a calendar year.
    Unearned = portion of written exposures not yet earned as of year end.
    """
    year_end = datetime(calendar_year, 12, 31)
    unearned = 0.0
    for row in exposure_table:
        q_date = parse_quarter(row['quarter'])
        policy_end = add_months(q_date, 12)
        if q_date <= year_end < policy_end:
            # Portion unearned = (policy_end - year_end) / 365.25
            unearned_months = (policy_end - year_end).days / 365.25
            unearned += row['written'] * min(max(unearned_months, 0), 1.0)
    return unearned


def calculate_quarter_earned_exposures(exposure_table: List[Dict[str, Any]], year: int, quarter: int) -> float:
    """
    Calculate earned exposures for a specific calendar quarter.
    """
    start = datetime(year, 3 * (quarter - 1) + 1, 1)
    if quarter < 4:
        end = datetime(year, 3 * quarter + 1, 1)
    else:
        end = datetime(year + 1, 1, 1)
    earned = 0.0
    for row in exposure_table:
        q_date = parse_quarter(row['quarter'])
        policy_end = add_months(q_date, 12)
        # Overlap between [q_date, policy_end) and [start, end)
        overlap_start = max(q_date, start)
        overlap_end = min(policy_end, end)
        if overlap_start < overlap_end:
            overlap_days = (overlap_end - overlap_start).days
            earned += row['written'] * (overlap_days / 365.25)
    return earned


__all__ = [
    'calculate_policy_year_earned_exposures',
    'calculate_in_force_exposures',
    'calculate_calendar_year_unearned_exposures',
    'calculate_quarter_earned_exposures',
]


__all__ = ['calculate_earned_exposure']
