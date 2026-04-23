import threading
from enum import Enum
from models.vehicle import Vehicle, VehicleType

class SpotType(Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'

class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: SpotType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.current_vehicle = None
        self._lock = threading.Lock()

    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        if self.spot_type == SpotType.SMALL:
            return vehicle.vehicle_type == VehicleType.BIKE

        elif self.spot_type == SpotType.MEDIUM:
            return vehicle.vehicle_type in [VehicleType.BIKE, VehicleType.CAR]

        elif self.spot_type == SpotType.LARGE:
            return True

        return False

    def is_available(self) -> bool:
        with self._lock:
            return not self.is_occupied

    def assign_vehicle(self, vehicle: Vehicle):
        with self._lock:
            if self.is_occupied:
                return False
            if not self.can_fit_vehicle(vehicle):
                return False

            self.is_occupied = True
            self.current_vehicle = vehicle
            return True

    def remove_vehicle(self):
        with self._lock:
            self.current_vehicle = None
            self.is_occupied = False
