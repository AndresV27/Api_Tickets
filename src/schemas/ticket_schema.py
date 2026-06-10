from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TicketStatus(str, Enum):
    created = "created"
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"

class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TicketBase(BaseModel):
    title: str
    description: str | None = None
    priority: TicketPriority 

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None
    priority: TicketPriority | None = None

class TicketResponse(TicketBase):
    id: int 
    status: TicketStatus
    user_id: int
    assigned_to: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class TicketAssign(BaseModel):
    assigned_to: int

