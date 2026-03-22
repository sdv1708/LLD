"""
models/vehicle.py
-----------------
Vehicle hierarchy using the Abstract Class pattern.

Design Decisions:
- Vehicle is an ABC that holds shared state (license_plate).
- Each subclass must implement get_size(), which drives spot-matching logic.
- Adding a new vehicle type (e.g. Bus) requires only a new subclass — zero
  changes to ParkingSpot, Level, or ParkingLot.  (Open/Closed Principle)
"""

from abc import ABC, abstractmethod


class Vehicle(ABC):
    """
    Abstract base class for all vehicle types.
    - Holds common state (license_plate)
    - Forces subclasses to declare their own size via get_size()
    """
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

    @abstractmethod
    def get_size(self) -> str:
        """Returns the size category: 'Small', 'Medium', or 'Large'."""
        pass


class Car(Vehicle):
    """Medium-sized vehicle; parks in Medium spots."""
    def get_size(self) -> str:
        return "Medium"


class Motorcycle(Vehicle):
    """Small-sized vehicle; parks in Small spots."""
    def get_size(self) -> str:
        return "Small"


class Truck(Vehicle):
    """Large-sized vehicle; parks in Large spots."""
    def get_size(self) -> str:
        return "Large"
