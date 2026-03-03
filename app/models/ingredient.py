from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    calories_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, nullable=False)
    carbs_per_100g = Column(Float, nullable=False)
    fat_per_100g = Column(Float, nullable=False)
    cost_per_100g = Column(Float, nullable=True)
    is_vegetarian = Column(Boolean, default=True)
    is_vegan = Column(Boolean, default=False)
    allergens = Column(String, nullable=True)

    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")