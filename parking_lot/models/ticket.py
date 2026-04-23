import datetime
from models.vehicle import Vehicle

class Ticket:
    def __init__(self, ticketId: int, vehicle: Vehicle, spot):
        self.ticketId = ticketId
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.datetime.now()
        self.exit_time = None
        self.payment_time = None
