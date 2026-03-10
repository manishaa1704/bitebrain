import asyncio
from mcp.server.fastmcp import FastMCP
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe

# Initialize FastMCP Server
mcp = FastMCP("BiteBrain API", dependencies=["sqlalchemy", "app"])

# Helper to get the database session
def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

@mcp.tool()
def get_ingredients() -> str:
    """Fetch all available ingredients in the BiteBrain database."""
    db = get_db()
    try:
        ingredients = db.query(Ingredient).all()
        result = "BiteBrain Ingredients:\n"
        for idx, i in enumerate(ingredients):
            result += f"{idx+1}. {i.name} ({i.calories_per_100g} kcal/100g)\n"
        return result
    finally:
        db.close()

@mcp.tool()
def get_recipes() -> str:
    """Fetch all recipes in the BiteBrain database and their ingredients."""
    db = get_db()
    try:
        recipes = db.query(Recipe).all()
        if not recipes:
            return "No recipes found."
            
        result = "BiteBrain Recipes:\n"
        for r in recipes:
            result += f"- {r.name} (Serves: {r.servings})\n"
            result += f"  Instructions: {r.instructions[:50]}...\n"
            if r.ingredients:
                result += "  Ingredients:\n"
                for ri in r.ingredients:
                    result += f"   * {ri.quantity_grams}g of {ri.ingredient.name}\n"
        return result
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    mcp.run(transport='stdio')
