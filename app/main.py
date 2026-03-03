from fastapi import FastAPI
from app.database import engine, Base
import app.models

app = FastAPI(
    title="BiteBrain API",
    description="A smart recipe and nutrition intelligence API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to BiteBrain API"}