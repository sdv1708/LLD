"""
main.py
-------
Entry point for the Parking Lot demo.

Run with:
    python main.py          (from inside the parking_lot/ directory)
    python -m parking_lot   (if parking_lot is treated as a package)
"""

from models import Car, Motorcycle, Truck
from models import ParkingSpot
from models import Ticket
from services import Level, PricingContext, WeekdayStrategy, WeekendStrategy, ParkingLot


def main():
    # ----------------------------------------------------------------
    # 1. Build the lot: 1 level, 3 spots of different sizes
    # ----------------------------------------------------------------
    spots = [
        ParkingSpot("S1", "Small"),
        ParkingSpot("M1", "Medium"),
        ParkingSpot("L1", "Large"),
    ]
    level1 = Level("Ground", spots)

    pricing = PricingContext(WeekdayStrategy(base_rate=5.0, hourly_rate=2.5))
    lot = ParkingLot(levels=[level1], pricing_context=pricing)

    # ----------------------------------------------------------------
    # 2. Singleton check — both references point to the same object
    # ----------------------------------------------------------------
    lot2 = ParkingLot(levels=[level1], pricing_context=pricing)
    print(f"Same instance: {lot is lot2}")   # Expected: True

    # ----------------------------------------------------------------
    # 3. Vehicle entry — fill all three spots
    # ----------------------------------------------------------------
    car   = Car("KA-01-1234")
    bike  = Motorcycle("MH-02-5678")
    truck = Truck("DL-03-9999")

    ticket  = lot.entry(car)    # → M1
    ticket2 = lot.entry(bike)   # → S1
    lot.entry(truck)            # → L1   (no ticket needed for demo)

    # ----------------------------------------------------------------
    # 4. Overflow test — lot is completely full
    # ----------------------------------------------------------------
    extra_car = Car("TN-04-1111")
    result = lot.entry(extra_car)   # No Medium spot available
    print(result)                   # Expected: "Parking Full!"

    # ----------------------------------------------------------------
    # 5. Switch pricing strategy mid-operation (Strategy pattern demo)
    # ----------------------------------------------------------------
    pricing.set_strategy(WeekendStrategy(flat_rate=10.0))

    # ----------------------------------------------------------------
    # 6. Vehicle exit — spot freed, fee calculated
    # ----------------------------------------------------------------
    if isinstance(ticket, Ticket):
        charge = lot.exit(ticket)
        print(f"Car charge:  ${charge:.2f}")

    if isinstance(ticket2, Ticket):
        charge2 = lot.exit(ticket2)
        print(f"Bike charge: ${charge2:.2f}")


if __name__ == "__main__":
    main()
