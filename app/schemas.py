from pydantic import BaseModel
from typing import Optional


class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str


class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    archived: bool

    class Config:
        from_attributes = True


class TodayHabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    archived: bool
    completed_today: bool
    current_streak: int
    best_streak: int        

class TodayHabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    archived: bool
    completed_today: bool
    current_streak: int
    best_streak: int    