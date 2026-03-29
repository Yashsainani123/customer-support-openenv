from pydantic import BaseModel
from typing import List

class Ticket(BaseModel):
    id: int
    issue: str
    priority: str
    status: str = "open"
    deadline: int = 5

class Agent(BaseModel):
    id: int
    department: str
    available: bool = True
    current_tasks: int = 0

class Observation(BaseModel):
    tickets: List[Ticket]
    agents: List[Agent]
    time: int

class Action(BaseModel):
    ticket_id: int
    assign_to: str
    response: str