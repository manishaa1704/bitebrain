from pydantic import BaseModel
from typing import Optional

class SubstitutionRequest(BaseModel):
    """Schema for requesting an ingredient substitution"""
    ingredient_name: str
    reason: str  # e.g. "vegan", "nut allergy", "lower calories", "cheaper"
    recipe_context: Optional[str] = "general cooking"