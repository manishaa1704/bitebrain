from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, ingredients, recipes, meal_plans, analytics
import app.models

app = FastAPI(
    title="BiteBrain API",
    description="A smart recipe and nutrition intelligence API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)
app.include_router(meal_plans.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to BiteBrain API"}