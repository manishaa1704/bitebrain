from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.meal_plan import MealPlan, MealPlanRecipe
from app.models.recipe import Recipe
from app.schemas.meal_plan import MealPlanCreate, MealPlanUpdate, MealPlanResponse, MealPlanRecipeAdd, MealPlanRecipeResponse
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/meal-plans", tags=["Meal Plans"])

@router.get("/", response_model=List[MealPlanResponse])
def get_my_meal_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all meal plans for the current user"""
    meal_plans = db.query(MealPlan).filter(MealPlan.owner_id == current_user.id).all()
    return meal_plans

@router.get("/{meal_plan_id}", response_model=MealPlanResponse)
def get_meal_plan(
    meal_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single meal plan by ID"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.owner_id == current_user.id
    ).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal plan with id {meal_plan_id} not found"
        )
    return meal_plan

@router.post("/", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
def create_meal_plan(
    meal_plan_data: MealPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new meal plan (requires authentication)"""
    meal_plan = MealPlan(
        name=meal_plan_data.name,
        description=meal_plan_data.description,
        owner_id=current_user.id
    )
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

@router.put("/{meal_plan_id}", response_model=MealPlanResponse)
def update_meal_plan(
    meal_plan_id: int,
    meal_plan_data: MealPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a meal plan (requires authentication)"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.owner_id == current_user.id
    ).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal plan with id {meal_plan_id} not found"
        )

    update_data = meal_plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal_plan, field, value)

    db.commit()
    db.refresh(meal_plan)
    return meal_plan

@router.delete("/{meal_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal_plan(
    meal_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a meal plan (requires authentication)"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.owner_id == current_user.id
    ).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal plan with id {meal_plan_id} not found"
        )

    db.delete(meal_plan)
    db.commit()
    return None

@router.post("/{meal_plan_id}/recipes", response_model=MealPlanRecipeResponse, status_code=status.HTTP_201_CREATED)
def add_recipe_to_meal_plan(
    meal_plan_id: int,
    recipe_data: MealPlanRecipeAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a recipe to a meal plan (requires authentication)"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.owner_id == current_user.id
    ).first()
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meal plan with id {meal_plan_id} not found"
        )

    recipe = db.query(Recipe).filter(Recipe.id == recipe_data.recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_data.recipe_id} not found"
        )

    meal_plan_recipe = MealPlanRecipe(
        meal_plan_id=meal_plan_id,
        recipe_id=recipe_data.recipe_id,
        day_of_week=recipe_data.day_of_week,
        meal_type=recipe_data.meal_type
    )
    db.add(meal_plan_recipe)
    db.commit()
    db.refresh(meal_plan_recipe)
    return meal_plan_recipe