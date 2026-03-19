from google import genai
from google.genai.errors import APIError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import json
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ingredient_substitutions(
        ingredient_name: str,
        reason: str,
        recipe_context: str,
        db: Session
) -> dict:
    """
    Use Google Gemini AI to suggest intelligent ingredient substitutions.

    Args:
        ingredient_name: The ingredient to substitute
        reason: Why substitution is needed (e.g. "vegan", "nut allergy", "cheaper")
        recipe_context: What recipe this ingredient is used in
        db: Database session to fetch existing ingredients
    """

    # Get all available ingredients from our database
    available_ingredients = db.query(Ingredient).all()
    ingredients_list = [
        {
            "name": i.name,
            "calories_per_100g": i.calories_per_100g,
            "protein_per_100g": i.protein_per_100g,
            "carbs_per_100g": i.carbs_per_100g,
            "fat_per_100g": i.fat_per_100g,
            "is_vegetarian": i.is_vegetarian,
            "is_vegan": i.is_vegan,
            "allergens": i.allergens,
            "cost_per_100g": i.cost_per_100g
        }
        for i in available_ingredients
        if i.name.lower() != ingredient_name.lower()
    ]

    prompt = f"""You are a professional nutritionist and chef assistant for BiteBrain, a nutrition intelligence API.

A user wants to substitute an ingredient in their recipe.

Ingredient to substitute: {ingredient_name}
Reason for substitution: {reason}
Recipe context: {recipe_context}

Available ingredients in our database:
{json.dumps(ingredients_list, indent=2)}

Please suggest the best substitutions. For each suggestion:
1. Prioritise ingredients already in our database
2. Also suggest ingredients not in our database if they would be better
3. Explain the nutritional impact of each substitution
4. Consider the cooking context

Respond ONLY with a valid JSON object in exactly this format:
{{
    "original_ingredient": "{ingredient_name}",
    "substitution_reason": "{reason}",
    "suggestions": [
        {{
            "name": "ingredient name",
            "in_database": true or false,
            "quantity_adjustment": "e.g. use same amount or use 80% of the amount",
            "reason": "why this is a good substitute",
            "nutritional_impact": "how this changes the nutrition",
            "cooking_notes": "any important cooking adjustments needed"
        }}
    ],
    "general_advice": "overall advice for this substitution"
}}"""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((APIError, Exception)),
        reraise=True
    )
    def _call_gemini():
        return client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

    response = _call_gemini()
    response_text = response.text

    # Clean up response in case there are markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()

    result = json.loads(response_text)
    return result