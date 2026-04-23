from models import Vehicle, VehicleType, ParkingSpot, SpotType
from services import ParkingFloor, HourlyPricingStrategy, ParkingLot

def main():
    spots = [
        ParkingSpot(1, SpotType.SMALL),
        ParkingSpot(2, SpotType.MEDIUM),
        ParkingSpot(3, SpotType.LARGE),
    ]
    floor1 = ParkingFloor(1, spots)

    pricing = HourlyPricingStrategy(rate_per_hour=2.5)
    lot = ParkingLot(floors=[floor1], pricing_strategy=pricing)

    car = Vehicle(101, VehicleType.CAR)
    bike = Vehicle(102, VehicleType.BIKE)
    truck = Vehicle(103, VehicleType.TRUCK)

    ticket1 = lot.park_vehicle(car)
    print(f"Parked car at spot {ticket1.spot.spot_id if ticket1 else 'N/A'}")

    ticket2 = lot.park_vehicle(bike)
    print(f"Parked bike at spot {ticket2.spot.spot_id if ticket2 else 'N/A'}")

    ticket3 = lot.park_vehicle(truck)
    print(f"Parked truck at spot {ticket3.spot.spot_id if ticket3 else 'N/A'}")

    extra_car = Vehicle(104, VehicleType.CAR)
    result_ticket = lot.park_vehicle(extra_car)
    if not result_ticket:
        print("Parking Full!")

    if ticket1:
        charge1 = lot.unpark_vehicle(ticket1)
        print(f"Car charge: ${charge1:.2f}")

    if ticket2:
        charge2 = lot.unpark_vehicle(ticket2)
        print(f"Bike charge: ${charge2:.2f}")

if __name__ == "__main__":
    main()
