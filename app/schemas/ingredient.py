from pydantic import BaseModel, field_validator
from typing import Optional

class IngredientCreate(BaseModel):
    name: str
    calories_per_100g: Optional[float] = None
    protein_per_100g: Optional[float] = None
    carbs_per_100g: Optional[float] = None
    fat_per_100g: Optional[float] = None
    cost_per_100g: Optional[float] = None
    is_vegetarian: bool = True
    is_vegan: bool = False
    allergens: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_must_be_valid(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Ingredient name must be at least 2 characters')
        if len(v) > 200:
            raise ValueError('Ingredient name cannot exceed 200 characters')
        return v.title()

    @field_validator('calories_per_100g')
    @classmethod
    def calories_must_be_valid(cls, v):
        if v is None:
            return v
        if v < 0:
            raise ValueError('Calories cannot be negative')
        if v > 900:
            raise ValueError('Calories per 100g cannot exceed 900')
        return v

    @field_validator('protein_per_100g', 'carbs_per_100g', 'fat_per_100g')
    @classmethod
    def macros_must_be_valid(cls, v):
        if v is None:
            return v
        if v < 0:
            raise ValueError('Macro values cannot be negative')
        if v > 100:
            raise ValueError('Macro values cannot exceed 100g per 100g')
        return v

    @field_validator('cost_per_100g')
    @classmethod
    def cost_must_be_valid(cls, v):
        if v is None:
            return v
        if v < 0:
            raise ValueError('Cost cannot be negative')
        if v > 1000:
            raise ValueError('Cost per 100g seems unreasonably high')
        return v


class IngredientUpdate(BaseModel):
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

    model_config = {"from_attributes": True}