from typing import List
from models.parking_spot import ParkingSpot
from models.vehicle import Vehicle

class ParkingFloor:
    def __init__(self, floor_id: int, spots: List[ParkingSpot]):
        self.floor_id = floor_id
        self.spots = spots

    def find_available_spot(self, vehicle: Vehicle) -> ParkingSpot:
        for spot in self.spots:
            if spot.assign_vehicle(vehicle):
                return spot

        return None
