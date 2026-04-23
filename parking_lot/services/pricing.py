from abc import ABC, abstractmethod
from models.ticket import Ticket

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        pass

class HourlyPricingStrategy(PricingStrategy):
    def __init__(self, rate_per_hour: float):
        self.rate_per_hour = rate_per_hour

    def calculate_fee(self, ticket: Ticket) -> float:
        duration_seconds = (ticket.exit_time - ticket.entry_time).total_seconds()
        hours = duration_seconds / 3600
        return hours * self.rate_per_hour
