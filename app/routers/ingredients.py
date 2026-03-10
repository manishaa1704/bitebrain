from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.get("/", response_model=List[IngredientResponse])
def get_all_ingredients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all ingredients with pagination"""
    ingredients = db.query(Ingredient).offset(skip).limit(limit).all()
    return ingredients

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Get a single ingredient by ID"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )
    return ingredient

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient_data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new ingredient (requires authentication)"""
    existing = db.query(Ingredient).filter(Ingredient.name == ingredient_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this name already exists"
        )
        
    ingredient_dict = ingredient_data.model_dump()
    
    # Check if we need to fetch from OpenFoodFacts
    needs_data = any(x is None for x in [
        ingredient_dict.get('calories_per_100g'),
        ingredient_dict.get('protein_per_100g'),
        ingredient_dict.get('carbs_per_100g'),
        ingredient_dict.get('fat_per_100g')
    ])
    
    if needs_data:
        import httpx
        try:
            # Search OpenFoodFacts UK database
            response = httpx.get(
                f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={ingredient_data.name}&search_simple=1&action=process&json=1&page_size=1",
                timeout=5.0
            )
            data = response.json()
            
            if data.get('products') and len(data['products']) > 0:
                product = data['products'][0]
                nutriments = product.get('nutriments', {})
                
                # Update missing fields with real-world data
                if ingredient_dict.get('calories_per_100g') is None:
                    kcal = nutriments.get('energy-kcal_100g')
                    ingredient_dict['calories_per_100g'] = float(kcal) if kcal is not None else 0.0
                    
                if ingredient_dict.get('protein_per_100g') is None:
                    protein = nutriments.get('proteins_100g')
                    ingredient_dict['protein_per_100g'] = float(protein) if protein is not None else 0.0
                    
                if ingredient_dict.get('carbs_per_100g') is None:
                    carbs = nutriments.get('carbohydrates_100g')
                    ingredient_dict['carbs_per_100g'] = float(carbs) if carbs is not None else 0.0
                    
                if ingredient_dict.get('fat_per_100g') is None:
                    fat = nutriments.get('fat_100g')
                    ingredient_dict['fat_per_100g'] = float(fat) if fat is not None else 0.0
                    
                # Optionally capture allergens if not provided
                if ingredient_dict.get('allergens') is None and product.get('allergens'):
                    ingredient_dict['allergens'] = product.get('allergens').replace('en:', '').replace(',', ', ')
                    
        except Exception as e:
            # If API fails or times out, default to 0.0 to prevent database errors
            if ingredient_dict.get('calories_per_100g') is None: ingredient_dict['calories_per_100g'] = 0.0
            if ingredient_dict.get('protein_per_100g') is None: ingredient_dict['protein_per_100g'] = 0.0
            if ingredient_dict.get('carbs_per_100g') is None: ingredient_dict['carbs_per_100g'] = 0.0
            if ingredient_dict.get('fat_per_100g') is None: ingredient_dict['fat_per_100g'] = 0.0

    ingredient = Ingredient(**ingredient_dict)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an ingredient (requires authentication)"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )

    # Only update fields that were actually provided
    update_data = ingredient_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an ingredient (requires authentication)"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with id {ingredient_id} not found"
        )

    db.delete(ingredient)
    db.commit()
    return None