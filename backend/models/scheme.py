from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class SchemeEligibility(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    min_age: Optional[int] = None
    max_age: Optional[int] = None
    max_income: Optional[float] = None

    occupations: List[str] = Field(
        default_factory=list,
        alias="occupation"
    )

    states: List[str] = Field(default_factory=list)

    categories: List[str] = Field(default_factory=list)

    min_land_acres: Optional[float] = None
    max_land_acres: Optional[float] = None

    genders: List[str] = Field(default_factory=list)

    education: List[str] = Field(default_factory=list)


class Scheme(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="scheme_id")
    name: str = Field(alias="scheme_name")

    category: str
    state: Optional[str] = None
    description: str

    eligibility: SchemeEligibility

    target_beneficiaries: Optional[List[str]] = None

    benefits: List[str]
    documents_required: List[str]

    how_to_apply: str

    official_link: str = Field(alias="official_source")

    status: str = "active"

    last_updated: Optional[str] = None