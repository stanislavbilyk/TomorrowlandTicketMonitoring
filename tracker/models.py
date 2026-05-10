from dataclasses import dataclass

@dataclass
class Ticket:
    id: int
    price: float
    type: int
