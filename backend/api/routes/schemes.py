from fastapi import APIRouter
from typing import List
from backend.models.scheme import Scheme
from backend.api.routes.chat import get_all_schemes

router = APIRouter()

@router.get("/schemes", response_model=List[Scheme])
async def get_schemes():
    """
    Retrieve all public government schemes.
    Returns only active schemes.
    """
    schemes = get_all_schemes()
    # Filter for only active schemes
    active_schemes = [s for s in schemes if s.status.lower() == "active"]
    return active_schemes
