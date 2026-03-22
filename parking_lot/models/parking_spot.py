"""
models/parking_spot.py
----------------------
Represents a single physical parking spot.

Key Design Decision — Query/Command Separation:
- can_fit_vehicle() is a QUERY  → reads state, never changes it
- assign_vehicle() is a COMMAND → changes state only after confirming fit
- This prevents a vehicle from accidentally occupying a spot during a search loop
  (the loop calls can_fit_vehicle repeatedly; only the winner calls assign_vehicle).
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.vehicle import Vehicle


class ParkingSpot:
    """
    Represents a single physical spot on a level.

    Attributes:
        spot_id   : Unique identifier, e.g. 'A1', 'B3'.
        spot_type : Size category ('Small', 'Medium', 'Large').
        is_occupied : True when a vehicle is currently parked here.
    """

    def __init__(self, spot_id: str, spot_type: str):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False

    def can_fit_vehicle(self, vehicle: "Vehicle") -> bool:
        """
        QUERY — does not modify state.
        Returns True only when the spot type matches the vehicle size
        AND the spot is currently free.
        """
        return self.spot_type == vehicle.get_size() and not self.is_occupied

    def assign_vehicle(self, vehicle: "Vehicle") -> bool:
        """
        COMMAND — marks spot as occupied if the vehicle fits.
        Returns True on success, False if the spot is incompatible or taken.
        """
        if self.can_fit_vehicle(vehicle):
            self.is_occupied = True
            return True
        return False

    def remove_vehicle(self):
        """Frees the spot when a vehicle exits."""
        self.is_occupied = False
