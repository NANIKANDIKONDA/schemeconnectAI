from typing import Optional
from pydantic import BaseModel

class CitizenProfile(BaseModel):
    age: Optional[int] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    annual_income: Optional[float] = None
    education: Optional[str] = None
    category: Optional[str] = None
    land_acres: Optional[float] = None
    gender: Optional[str] = None
    beneficiary_for: Optional[str] = None
    user_intent: Optional[str] = None
