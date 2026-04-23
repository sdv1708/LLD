import datetime
import threading
from typing import List
from models.vehicle import Vehicle
from models.ticket import Ticket
from services.parking_floor import ParkingFloor
from services.pricing import PricingStrategy

class ParkingLot:
    def __init__(self, floors: List[ParkingFloor], pricing_strategy: PricingStrategy):
        self.floors = floors
        self.ticket_counter = 0
        self.pricing_strategy = pricing_strategy
        self._ticket_lock = threading.Lock()

    def next_ticket_id(self):
        with self._ticket_lock:
            self.ticket_counter += 1
            return self.ticket_counter

    def park_vehicle(self, vehicle: Vehicle):
        for floor in self.floors:
            spot = floor.find_available_spot(vehicle)
            if spot:
                ticket = Ticket(
                    ticketId=self.next_ticket_id(),
                    vehicle=vehicle,
                    spot=spot
                )
                return ticket

        return None

    def unpark_vehicle(self, ticket: Ticket):
        spot = ticket.spot
        spot.remove_vehicle()

        exit_time = datetime.datetime.now()
        ticket.exit_time = exit_time

        fee = self.pricing_strategy.calculate_fee(ticket)
        return fee
