"""
services/parking_lot.py
-----------------------
The central ParkingLot system — implemented as a Singleton.

Singleton Mechanism (Thread-Safe Double-Checked Locking):
1. __new__ intercepts every construction attempt.
2. First check  (outside lock) — fast path once the instance exists; avoids
   acquiring the lock on every call after the first.
3. Lock acquisition — only one thread proceeds into the critical section.
4. Second check (inside lock) — guards against the race where two threads both
   pass the first check before either creates the instance.

This is the canonical thread-safe Singleton pattern in Python.
"""

import datetime
import threading
from typing import Optional, Union

from models.vehicle import Vehicle
from models.parking_spot import ParkingSpot
from models.ticket import Ticket
from services.level import Level
from services.pricing import PricingContext


class ParkingLot:
    """
    Central parking-lot system — exactly one instance exists (Singleton).

    Responsibilities:
    - Accept incoming vehicles (entry) and issue Tickets.
    - Free spots and calculate charges when vehicles leave (exit).
    - Delegate spot-search and pricing to Level and PricingContext.
    """

    _instance = None
    _lock = threading.Lock()

    # ------------------------------------------------------------------
    # Singleton construction
    # ------------------------------------------------------------------

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:               # First check (no lock)
            with cls._lock:
                if cls._instance is None:       # Second check (inside lock)
                    cls._instance = super().__new__(cls)
                    print("ParkingLot instance created.")
        return cls._instance

    def __init__(self, levels: list[Level], pricing_context: PricingContext):
        self.levels = levels
        self.pricing_context = pricing_context

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_spot_by_id(self, spot_id: str) -> Optional[ParkingSpot]:
        """Traverse all levels to locate a spot by its ID."""
        for level in self.levels:
            for spot in level.spots:
                if spot.spot_id == spot_id:
                    return spot
        return None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def entry(self, vehicle: Vehicle) -> Union[Ticket, str]:
        """
        Vehicle arrives → find a spot across all levels → issue a Ticket.

        Iterates levels in order; returns the Ticket of the first available
        spot, or the string "Parking Full!" when no level has room.
        """
        for level in self.levels:
            parked_spot = level.park_vehicle(vehicle)
            if parked_spot:
                ticket = Ticket(vehicle, parked_spot.spot_id)
                print(f"Vehicle {vehicle.license_plate} parked at spot {parked_spot.spot_id}")
                return ticket
        return "Parking Full!"

    def exit(self, ticket: Ticket) -> float:
        """
        Vehicle leaves → record exit time → free the spot → calculate charge.

        Returns the total parking fee (float, dollars).
        """
        ticket.exit_time = datetime.datetime.now()

        spot = self._find_spot_by_id(ticket.spot_id)
        if spot:
            spot.remove_vehicle()

        duration = ticket.exit_time - ticket.entry_time
        total = self.pricing_context.calculate_parking_total(duration=duration)
        return total
