from fastapi import status

def test_get_all_ingredients_empty(client):
    response = client.get("/ingredients/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_create_ingredient(client):
    ingredient_data = {
        "name": "Tomato",
        "calories_per_100g": 18.0,
        "protein_per_100g": 0.9,
        "carbs_per_100g": 3.9,
        "fat_per_100g": 0.2,
        "is_vegetarian": True
    }
    response = client.post("/ingredients/", json=ingredient_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Tomato"
    assert data["id"] is not None

def test_create_duplicate_ingredient(client):
    ingredient_data = {
        "name": "Onion",
        "calories_per_100g": 40.0,
        "protein_per_100g": 1.1,
        "carbs_per_100g": 9.3,
        "fat_per_100g": 0.1,
        "is_vegetarian": True
    }
    client.post("/ingredients/", json=ingredient_data)
    response = client.post("/ingredients/", json=ingredient_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Ingredient with this name already exists"

def test_get_ingredient(client):
    ingredient_data = {
        "name": "Chicken Breast",
        "calories_per_100g": 165.0,
        "protein_per_100g": 31.0,
        "carbs_per_100g": 0.0,
        "fat_per_100g": 3.6,
        "is_vegetarian": False
    }
    create_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = create_response.json()["id"]

    response = client.get(f"/ingredients/{ingredient_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Chicken Breast"

def test_get_nonexistent_ingredient(client):
    response = client.get("/ingredients/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_ingredient(client):
    ingredient_data = {
        "name": "Beef",
        "calories_per_100g": 250.0,
        "protein_per_100g": 26.0,
        "carbs_per_100g": 0.0,
        "fat_per_100g": 15.0,
        "is_vegetarian": False
    }
    create_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = create_response.json()["id"]

    update_data = {
        "is_vegetarian": True # testing update
    }
    response = client.put(f"/ingredients/{ingredient_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_vegetarian"] == True
    assert response.json()["name"] == "Beef" # name shouldn't change

def test_delete_ingredient(client):
    ingredient_data = {
        "name": "Pork",
        "calories_per_100g": 242.0,
        "protein_per_100g": 27.0,
        "carbs_per_100g": 0.0,
        "fat_per_100g": 14.0,
        "is_vegetarian": False
    }
    create_response = client.post("/ingredients/", json=ingredient_data)
    ingredient_id = create_response.json()["id"]

    response = client.delete(f"/ingredients/{ingredient_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's gone
    get_response = client.get(f"/ingredients/{ingredient_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
