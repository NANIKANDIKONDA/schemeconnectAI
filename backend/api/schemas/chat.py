from pydantic import BaseModel, Field, constr
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=2000, description="The user's message")

class SchemeResult(BaseModel):
    name: str
    category: str
    eligibility_status: str
    relevance: str
    matched_conditions: int
    missing_information: List[str]
    failed_conditions: List[str]
    success_reasons: List[str] = []
    benefits: List[str] = []
    documents_required: List[str] = []
    how_to_apply: Optional[str] = None
    official_url: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    response_type: str
    message: str
    profile: Dict[str, Any]
    missing_information: List[str]
    schemes: Optional[List[SchemeResult]] = None
