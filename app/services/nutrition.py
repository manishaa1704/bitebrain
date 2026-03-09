from sqlalchemy.orm import Session
from app.models.recipe import Recipe, RecipeIngredient
from app.models.ingredient import Ingredient
from typing import Optional


def calculate_recipe_macros(recipe_id: int, db: Session) -> Optional[dict]:
    """Calculate full macro breakdown for a recipe"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        return None

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_cost = 0
    total_grams = 0
    has_cost_data = True

    ingredient_breakdown = []

    for ri in recipe.ingredients:
        ingredient = ri.ingredient
        factor = ri.quantity_grams / 100  # Convert from per-100g to actual quantity

        cal = ingredient.calories_per_100g * factor
        protein = ingredient.protein_per_100g * factor
        carbs = ingredient.carbs_per_100g * factor
        fat = ingredient.fat_per_100g * factor

        total_calories += cal
        total_protein += protein
        total_carbs += carbs
        total_fat += fat
        total_grams += ri.quantity_grams

        if ingredient.cost_per_100g is not None:
            total_cost += ingredient.cost_per_100g * factor
        else:
            has_cost_data = False

        ingredient_breakdown.append({
            "ingredient": ingredient.name,
            "quantity_grams": ri.quantity_grams,
            "calories": round(cal, 2),
            "protein_g": round(protein, 2),
            "carbs_g": round(carbs, 2),
            "fat_g": round(fat, 2)
        })

    per_serving_calories = total_calories / recipe.servings

    return {
        "recipe_id": recipe_id,
        "recipe_name": recipe.name,
        "servings": recipe.servings,
        "total_weight_grams": round(total_grams, 2),
        "total_nutrition": {
            "calories": round(total_calories, 2),
            "protein_g": round(total_protein, 2),
            "carbs_g": round(total_carbs, 2),
            "fat_g": round(total_fat, 2),
        },
        "per_serving": {
            "calories": round(per_serving_calories, 2),
            "protein_g": round(total_protein / recipe.servings, 2),
            "carbs_g": round(total_carbs / recipe.servings, 2),
            "fat_g": round(total_fat / recipe.servings, 2),
        },
        "estimated_cost": round(total_cost, 2) if has_cost_data else None,
        "ingredient_breakdown": ingredient_breakdown
    }


def get_recipe_allergens(recipe_id: int, db: Session) -> Optional[dict]:
    """Get all allergens present in a recipe"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        return None

    allergens_found = set()
    ingredients_with_allergens = []

    for ri in recipe.ingredients:
        ingredient = ri.ingredient
        if ingredient.allergens:
            allergen_list = [a.strip() for a in ingredient.allergens.split(",")]
            allergens_found.update(allergen_list)
            ingredients_with_allergens.append({
                "ingredient": ingredient.name,
                "allergens": allergen_list
            })

    return {
        "recipe_id": recipe_id,
        "recipe_name": recipe.name,
        "contains_allergens": len(allergens_found) > 0,
        "allergens": sorted(list(allergens_found)),
        "ingredients_with_allergens": ingredients_with_allergens,
        "is_vegetarian": all(ri.ingredient.is_vegetarian for ri in recipe.ingredients),
        "is_vegan": all(ri.ingredient.is_vegan for ri in recipe.ingredients)
    }


def get_popular_ingredients(db: Session, limit: int = 10) -> list:
    """Get most used ingredients across all recipes"""
    from sqlalchemy import func

    results = (
        db.query(
            Ingredient.name,
            Ingredient.calories_per_100g,
            func.count(RecipeIngredient.id).label("usage_count"),
            func.sum(RecipeIngredient.quantity_grams).label("total_grams_used")
        )
        .join(RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id)
        .group_by(Ingredient.id, Ingredient.name, Ingredient.calories_per_100g)
        .order_by(func.count(RecipeIngredient.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "ingredient": r.name,
            "calories_per_100g": r.calories_per_100g,
            "used_in_recipes": r.usage_count,
            "total_grams_used": round(r.total_grams_used, 2)
        }
        for r in results
    ]


def get_nutrition_summary(db: Session) -> dict:
    """Get a high level summary of all nutrition data in the system"""
    from sqlalchemy import func

    total_recipes = db.query(Recipe).count()
    total_ingredients = db.query(Ingredient).count()

    vegetarian_count = db.query(Ingredient).filter(
        Ingredient.is_vegetarian == True
    ).count()

    vegan_count = db.query(Ingredient).filter(
        Ingredient.is_vegan == True
    ).count()

    avg_calories = db.query(
        func.avg(Ingredient.calories_per_100g)
    ).scalar()

    return {
        "total_recipes": total_recipes,
        "total_ingredients": total_ingredients,
        "vegetarian_ingredients": vegetarian_count,
        "vegan_ingredients": vegan_count,
        "avg_calories_per_100g": round(avg_calories, 2) if avg_calories else 0,
    }