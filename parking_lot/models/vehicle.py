from enum import Enum

class VehicleType(Enum):
    CAR = 'car'
    BIKE = 'bike'
    TRUCK = 'truck'

class Vehicle:
    def __init__(self, vehicle_id: int, vehicle_type: VehicleType):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type

    def get_vehicle_id(self):
        return self.vehicle_id

    def get_vehicle_type(self):
        return self.vehicle_type
