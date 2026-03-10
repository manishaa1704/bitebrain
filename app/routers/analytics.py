from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.nutrition import (
    calculate_recipe_macros,
    get_recipe_allergens,
    get_popular_ingredients,
    get_nutrition_summary
)
from app.services.ai_substitution import get_ingredient_substitutions
from app.schemas.analytics import SubstitutionRequest
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/recipe/{recipe_id}/macros")
def get_recipe_macros(recipe_id: int, db: Session = Depends(get_db)):
    """Get full macro breakdown for a recipe.
    Returns calories, protein, carbs and fat both total and per serving."""
    result = calculate_recipe_macros(recipe_id, db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return result


@router.get("/recipe/{recipe_id}/allergens")
def get_allergens(recipe_id: int, db: Session = Depends(get_db)):
    """Get allergen warnings for a recipe.
    Also returns vegetarian and vegan status."""
    result = get_recipe_allergens(recipe_id, db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return result


@router.get("/recipe/{recipe_id}/cost")
def get_recipe_cost(recipe_id: int, db: Session = Depends(get_db)):
    """Get estimated cost breakdown for a recipe."""
    result = calculate_recipe_macros(recipe_id, db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return {
        "recipe_id": recipe_id,
        "recipe_name": result["recipe_name"],
        "servings": result["servings"],
        "total_estimated_cost": result["estimated_cost"],
        "cost_per_serving": round(result["estimated_cost"] / result["servings"], 2) if result["estimated_cost"] else None,
        "ingredient_breakdown": [
            {
                "ingredient": i["ingredient"],
                "quantity_grams": i["quantity_grams"],
            }
            for i in result["ingredient_breakdown"]
        ]
    }


@router.get("/trends/popular-ingredients")
def popular_ingredients(limit: int = 10, db: Session = Depends(get_db)):
    """Get the most frequently used ingredients across all recipes."""
    results = get_popular_ingredients(db, limit)
    if not results:
        return {"message": "No ingredient usage data yet", "data": []}
    return {"popular_ingredients": results}


@router.get("/summary")
def nutrition_summary(db: Session = Depends(get_db)):
    """Get a high level summary of all nutrition data in the system."""
    return get_nutrition_summary(db)


@router.post("/substitute")
def substitute_ingredient(
    request: SubstitutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    AI-powered ingredient substitution suggestions.
    Uses Gemini AI to suggest the best substitutes based on your reason
    (e.g. vegan, allergy, lower calories, cheaper).
    Requires authentication.
    """
    try:
        result = get_ingredient_substitutions(
            ingredient_name=request.ingredient_name,
            reason=request.reason,
            recipe_context=request.recipe_context,
            db=db
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI substitution failed: {str(e)}"
        )