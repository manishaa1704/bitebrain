from fastapi import status

def test_get_all_recipes_empty(client):
    response = client.get("/recipes/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_create_recipe(client):
    ingredient_data = {
        "name": "Egg",
        "calories_per_100g": 155.0,
        "protein_per_100g": 13.0,
        "carbs_per_100g": 1.1,
        "fat_per_100g": 11.0,
        "is_vegetarian": False
    }
    ing_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = ing_response.json()["id"]

    recipe_data = {
        "name": "Boiled Egg",
        "description": "Simple boiled egg",
        "instructions": "Boil water, add egg, wait 7 mins",
        "servings": 1,
        "ingredients": [
            {
                "ingredient_id": ingredient_id,
                "quantity_grams": 50.0
            }
        ]
    }
    response = client.post("/recipes/", json=recipe_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Boiled Egg"
    assert data["id"] is not None
    assert len(data["ingredients"]) == 1

def test_get_recipe(client):
    recipe_data = {
        "name": "Toast",
        "description": "Bread toast",
        "instructions": "Toast bread",
        "servings": 1,
        "ingredients": []
    }
    create_response = client.post("/recipes/", json=recipe_data)
    recipe_id = create_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Toast"

def test_get_nonexistent_recipe(client):
    response = client.get("/recipes/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_recipe(client):
    recipe_data = {
        "name": "Water",
        "description": "Glass of water",
        "instructions": "Pour water",
        "servings": 1,
        "ingredients": []
    }
    create_response = client.post("/recipes/", json=recipe_data)
    recipe_id = create_response.json()["id"]

    update_data = {
        "servings": 2
    }
    response = client.put(f"/recipes/{recipe_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["servings"] == 2

def test_delete_recipe(client):
    recipe_data = {
        "name": "Air",
        "description": "Breath of air",
        "instructions": "Breathe in",
        "servings": 1,
        "ingredients": []
    }
    create_response = client.post("/recipes/", json=recipe_data)
    recipe_id = create_response.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_add_ingredient_to_recipe(client):
    # 1. create recipe
    recipe_data = {
        "name": "Salt Water",
        "description": "Salty",
        "instructions": "Mix",
        "servings": 1,
        "ingredients": []
    }
    recipe_resp = client.post("/recipes/", json=recipe_data)
    recipe_id = recipe_resp.json()["id"]

    # 2. create ingredient
    ing_data = {
        "name": "Salt",
        "calories_per_100g": 0.0,
        "protein_per_100g": 0.0,
        "carbs_per_100g": 0.0,
        "fat_per_100g": 0.0,
        "is_vegetarian": True
    }
    ing_resp = client.post("/ingredients/", json=ing_data)
    ing_id = ing_resp.json()["id"]

    # 3. add ingredient
    add_data = {
        "ingredient_id": ing_id,
        "quantity_grams": 5.0
    }
    response = client.post(f"/recipes/{recipe_id}/ingredients", json=add_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["ingredient"]["name"] == "Salt"
    assert response.json()["quantity_grams"] == 5.0
