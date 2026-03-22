"""
services/level.py
-----------------
Represents a single floor of the parking structure.

Responsibilities:
- Iterate over its spots to find a compatible, vacant one.
- Delegate to ParkingSpot for the actual assignment.

Design Note:
- find_available_spot() is a pure search (query) — it reads but never writes.
- park_vehicle() is the command that wires the query result into a state change.
Separating the two makes the Level easier to test in isolation.
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.vehicle import Vehicle
    from models.parking_spot import ParkingSpot

from models.parking_spot import ParkingSpot
from models.vehicle import Vehicle


class Level:
    """
    Represents one floor of the parking structure.

    Attributes:
        level_id : Human-readable identifier, e.g. 'Ground', 'B1'.
        spots    : Ordered list of ParkingSpot objects on this floor.
    """

    def __init__(self, level_id: str, spots: list[ParkingSpot]):
        self.level_id = level_id
        self.spots = spots

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        QUERY — scans spots and returns the first compatible, free one.
        Does NOT assign the vehicle; that is the caller's responsibility.
        """
        for spot in self.spots:
            if spot.can_fit_vehicle(vehicle):
                return spot
        return None

    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        COMMAND — finds a spot and assigns it atomically.
        Returns the assigned spot, or None if no compatible spot is free.
        """
        spot = self.find_available_spot(vehicle)
        if spot:
            spot.assign_vehicle(vehicle)
            return spot
        return None
