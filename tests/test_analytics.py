import pytest
import json
from unittest.mock import patch, MagicMock
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

@patch('app.services.ai_substitution.client')
def test_substitute_ingredient(mock_client, client):
    """Test AI substitution endpoint with mocked Gemini client"""

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

    # Mock the new google-genai client response
    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_response_data)
    mock_client.models.generate_content.return_value = mock_response

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
    assert mock_client.models.generate_content.called