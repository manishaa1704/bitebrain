from pydantic import BaseModel
from typing import Optional

class IngredientCreate(BaseModel):
    """Schema for creating an ingredient"""
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    cost_per_100g: Optional[float] = None
    is_vegetarian: bool = True
    is_vegan: bool = False
    allergens: Optional[str] = None

class IngredientUpdate(BaseModel):
    """Schema for updating an ingredient - all fields optional"""
    name: Optional[str] = None
    calories_per_100g: Optional[float] = None
    protein_per_100g: Optional[float] = None
    carbs_per_100g: Optional[float] = None
    fat_per_100g: Optional[float] = None
    cost_per_100g: Optional[float] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    allergens: Optional[str] = None

class IngredientResponse(BaseModel):
    """Schema for returning ingredient data"""
    id: int
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    cost_per_100g: Optional[float]
    is_vegetarian: bool
    is_vegan: bool
    allergens: Optional[str]

    class Config:
        from_attributes = True