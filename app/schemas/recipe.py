from pydantic import BaseModel
from typing import Optional, List
from app.schemas.ingredient import IngredientResponse

class RecipeIngredientAdd(BaseModel):
    """Schema for adding an ingredient to a recipe"""
    ingredient_id: int
    quantity_grams: float

class RecipeIngredientResponse(BaseModel):
    """Schema for returning a recipe ingredient"""
    id: int
    ingredient_id: int
    quantity_grams: float
    ingredient: IngredientResponse

    model_config = {"from_attributes": True}

class RecipeCreate(BaseModel):
    """Schema for creating a recipe"""
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    servings: int = 1
    ingredients: List[RecipeIngredientAdd] = []

class RecipeUpdate(BaseModel):
    """Schema for updating a recipe"""
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    servings: Optional[int] = None

class RecipeResponse(BaseModel):
    """Schema for returning a recipe"""
    id: int
    name: str
    description: Optional[str]
    instructions: Optional[str]
    servings: int
    ingredients: List[RecipeIngredientResponse] = []

    model_config = {"from_attributes": True}