from pydantic import BaseModel
from typing import Optional, List

class MealPlanRecipeAdd(BaseModel):
    """Schema for adding a recipe to a meal plan"""
    recipe_id: int
    day_of_week: Optional[str] = None
    meal_type: Optional[str] = None

class MealPlanRecipeResponse(BaseModel):
    """Schema for returning a meal plan recipe"""
    id: int
    recipe_id: int
    day_of_week: Optional[str]
    meal_type: Optional[str]

    class Config:
        from_attributes = True

class MealPlanCreate(BaseModel):
    """Schema for creating a meal plan"""
    name: str
    description: Optional[str] = None

class MealPlanUpdate(BaseModel):
    """Schema for updating a meal plan"""
    name: Optional[str] = None
    description: Optional[str] = None

class MealPlanResponse(BaseModel):
    """Schema for returning a meal plan"""
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    recipes: List[MealPlanRecipeResponse] = []

    class Config:
        from_attributes = True