"""
models/ticket.py
----------------
Parking ticket issued on entry, used for billing on exit.

Design Notes:
- entry_time is set automatically at construction (no manual injection needed).
- exit_time starts as None and is stamped by ParkingLot.exit().
- Keeping billing data together on the Ticket avoids passing vehicle/spot
  references around after parking occurs.
"""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.vehicle import Vehicle


class Ticket:
    """
    Issued on vehicle entry. Carries all data required for billing on exit.

    Attributes:
        vehicle_number : License plate captured at entry.
        vehicle_type   : Size category captured at entry (for billing tiers).
        spot_id        : Which spot was assigned.
        entry_time     : Auto-stamped at object creation.
        exit_time      : Set by ParkingLot.exit(); None until then.
    """

    def __init__(self, vehicle: "Vehicle", spot_id: str):
        self.vehicle_number = vehicle.license_plate
        self.vehicle_type = vehicle.get_size()
        self.spot_id = spot_id
        self.entry_time = datetime.datetime.now()
        self.exit_time = None
