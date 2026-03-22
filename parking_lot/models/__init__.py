# parking_lot/models/__init__.py
# Makes 'models' a package and re-exports the public API.

from models.vehicle import Vehicle, Car, Motorcycle, Truck
from models.parking_spot import ParkingSpot
from models.ticket import Ticket

__all__ = [
    "Vehicle", "Car", "Motorcycle", "Truck",
    "ParkingSpot",
    "Ticket",
]
