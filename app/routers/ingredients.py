from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.get("/", response_model=List[IngredientResponse])
def get_all_ingredients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all ingredients with pagination"""
    ingredients = db.query(Ingredient).offset(skip).limit(limit).all()
    return ingredients

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Get a single ingredient by ID"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )
    return ingredient

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient_data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new ingredient (requires authentication)"""
    existing = db.query(Ingredient).filter(Ingredient.name == ingredient_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this name already exists"
        )

    ingredient = Ingredient(**ingredient_data.model_dump())
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an ingredient (requires authentication)"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )

    # Only update fields that were actually provided
    update_data = ingredient_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an ingredient (requires authentication)"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )

    db.delete(ingredient)
    db.commit()
    return None