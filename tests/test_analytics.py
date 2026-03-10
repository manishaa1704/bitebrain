import pytest
from unittest.mock import patch
from fastapi import status

def test_get_nutrition_summary(client):
    response = client.get("/analytics/summary")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_recipes" in data
    assert "total_ingredients" in data

def test_popular_ingredients_empty(client):
    response = client.get("/analytics/trends/popular-ingredients")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()

@patch('app.services.ai_substitution.genai.GenerativeModel.generate_content')
def test_substitute_ingredient(mock_generate_content, client):
    # Mock the Gemini API response
    class MockResponse:
        def __init__(self, text):
            self.text = text

    mock_response_data = {
        "original_ingredient": "butter",
        "substitution_reason": "vegan",
        "suggestions": [
            {
                "name": "coconut oil",
                "in_database": False,
                "quantity_adjustment": "use same amount",
                "reason": "good vegan fat substitute",
                "nutritional_impact": "similar calories, different fat profile",
                "cooking_notes": "melts easily"
            }
        ],
        "general_advice": "coconut oil works well for baking"
    }

    import json
    mock_generate_content.return_value = MockResponse(
        text=f"```json\n{json.dumps(mock_response_data)}\n```"
    )

    request_data = {
        "ingredient_name": "butter",
        "reason": "vegan",
        "recipe_context": "baking a cake"
    }
    
    response = client.post("/analytics/substitute", json=request_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["original_ingredient"] == "butter"
    assert len(data["suggestions"]) == 1
    assert mock_generate_content.called
