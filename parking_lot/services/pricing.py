"""
services/pricing.py
-------------------
Strategy pattern for flexible parking-fee calculation.

Why Strategy?
- ParkingLot depends only on PricingStrategy (the interface), never on a
  concrete class.  Swapping pricing rules at runtime is a one-liner:
      pricing_context.set_strategy(WeekendStrategy(flat_rate=10))
- Adding a new pricing rule (e.g. NightRateStrategy) requires only a new class
  — zero changes to ParkingLot.  (Open/Closed Principle)

Classes:
  PricingStrategy  — ABC; defines the calculate_cost() contract.
  WeekdayStrategy  — base rate for the first hour, then per-hour beyond that.
  WeekendStrategy  — flat rate regardless of duration.
  PricingContext   — holds the active strategy; normalises timedelta → hours.
"""

import datetime
from abc import ABC, abstractmethod
from typing import Optional, Union


# ---------------------------------------------------------------------------
# Abstract strategy
# ---------------------------------------------------------------------------

class PricingStrategy(ABC):
    """
    Abstract base for all pricing strategies.
    ParkingLot depends on this interface — not on any concrete strategy.
    """
    @abstractmethod
    def calculate_cost(self, duration: Optional[float] = None) -> float:
        """
        Compute the fee.

        Args:
            duration: Parking duration in hours (float).  May be None for
                      strategies that ignore duration (e.g. flat rate).
        Returns:
            Fee in dollars (float).
        """
        pass


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class WeekdayStrategy(PricingStrategy):
    """
    Base rate for the first hour, then hourly_rate per additional hour.

    Example: base_rate=5, hourly_rate=2.5 → 2-hour stay costs $7.50
    """
    def __init__(self, base_rate: float, hourly_rate: float):
        self.base_rate = base_rate
        self.hourly_rate = hourly_rate

    def calculate_cost(self, duration: Optional[float] = None) -> float:
        if duration is None or duration <= 1:
            return self.base_rate
        return self.base_rate + (duration - 1) * self.hourly_rate


class WeekendStrategy(PricingStrategy):
    """Flat rate regardless of duration — used on weekends."""
    def __init__(self, flat_rate: float):
        self.flat_rate = flat_rate

    def calculate_cost(self, duration: Optional[float] = None) -> float:
        return self.flat_rate


# ---------------------------------------------------------------------------
# Context (holds and delegates to the active strategy)
# ---------------------------------------------------------------------------

class PricingContext:
    """
    Wrapper that holds the active strategy and handles
    duration type conversion (timedelta → float hours).

    Usage:
        ctx = PricingContext(WeekdayStrategy(5.0, 2.5))
        ctx.set_strategy(WeekendStrategy(10.0))   # swap at runtime
        cost = ctx.calculate_parking_total(duration=timedelta(hours=2))
    """

    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PricingStrategy):
        """Swap the active pricing strategy at runtime."""
        print(f"Strategy changed to: {strategy.__class__.__name__}")
        self.strategy = strategy

    def calculate_parking_total(
        self,
        duration: Union[datetime.timedelta, float, None] = None
    ) -> float:
        """
        Normalise duration and delegate to the active strategy.

        Args:
            duration: Either a timedelta, a float (hours), or None.
        Returns:
            Total parking fee in dollars.
        """
        if self.strategy is None:
            raise ValueError("No pricing strategy set.")

        # Normalise to hours (float)
        if isinstance(duration, datetime.timedelta):
            duration_hours = duration.total_seconds() / 3600
        else:
            duration_hours = duration

        cost = self.strategy.calculate_cost(duration_hours)
        print(f"Parking cost: ${cost:.2f}")
        return cost
