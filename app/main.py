from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import engine, Base
from app.routers import auth, ingredients, recipes, meal_plans, analytics
import app.models

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="BiteBrain API",
    description="A smart recipe and nutrition intelligence API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)
app.include_router(meal_plans.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to BiteBrain API"}