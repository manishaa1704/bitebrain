from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="meal_plans")
    recipes = relationship("MealPlanRecipe", back_populates="meal_plan")


class MealPlanRecipe(Base):
    __tablename__ = "meal_plan_recipes"

    id = Column(Integer, primary_key=True, index=True)
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    day_of_week = Column(String, nullable=True)  # e.g. "Monday", "Tuesday"
    meal_type = Column(String, nullable=True)     # e.g. "breakfast", "lunch", "dinner"

    meal_plan = relationship("MealPlan", back_populates="recipes")
    recipe = relationship("Recipe", back_populates="meal_plan_recipes")