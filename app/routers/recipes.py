from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.recipe import Recipe, RecipeIngredient
from app.models.ingredient import Ingredient
from app.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse, RecipeIngredientAdd, RecipeIngredientResponse
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/", response_model=List[RecipeResponse])
def get_all_recipes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all recipes"""
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a single recipe by ID"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return recipe

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe with ingredients (requires authentication)"""
    recipe = Recipe(
        name=recipe_data.name,
        description=recipe_data.description,
        instructions=recipe_data.instructions,
        servings=recipe_data.servings
    )
    db.add(recipe)
    db.flush()  # Get the recipe ID without fully committing

    # Add ingredients to the recipe
    for ingredient_data in recipe_data.ingredients:
        ingredient = db.query(Ingredient).filter(
            Ingredient.id == ingredient_data.ingredient_id
        ).first()
        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with id {ingredient_data.ingredient_id} not found"
            )
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient_data.ingredient_id,
            quantity_grams=ingredient_data.quantity_grams
        )
        db.add(recipe_ingredient)

    db.commit()
    db.refresh(recipe)
    return recipe

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a recipe (requires authentication)"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )

    update_data = recipe_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recipe, field, value)

    db.commit()
    db.refresh(recipe)
    return recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a recipe (requires authentication)"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )

    db.delete(recipe)
    db.commit()
    return None

@router.post("/{recipe_id}/ingredients", response_model=RecipeIngredientResponse, status_code=status.HTTP_201_CREATED)
def add_ingredient_to_recipe(
    recipe_id: int,
    ingredient_data: RecipeIngredientAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add an ingredient to an existing recipe (requires authentication)"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_data.ingredient_id
    ).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_data.ingredient_id} not found"
        )

    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=ingredient_data.ingredient_id,
        quantity_grams=ingredient_data.quantity_grams
    )
    db.add(recipe_ingredient)
    db.commit()
    db.refresh(recipe_ingredient)
    return recipe_ingredient