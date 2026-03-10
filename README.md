# BiteBrain API
A smart recipe and nutrition intelligence API built for the COMP3011 Web Services API Development coursework.

## Overview
BiteBrain is a RESTful API designed to manage ingredients, recipes, and personalized meal plans while providing nutritional analytics. It enables full CRUD functionality on a SQLite database. 

## Technical Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Alembic
- **Testing**: Pytest

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <your-repo-link>
   cd bitebrain
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations (Optional if bitebrain.db already exists)**:
   ```bash
   alembic upgrade head
   ```

5. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. 
   Swagger UI documentation is available at `http://127.0.0.1:8000/docs`.

## Running Tests
To run the test suite, ensure your virtual environment is activated and run:
```bash
PYTHONPATH=. pytest tests/ -v
```

## API Documentation
The formal API documentation is available in [API_Documentation.pdf](./API_Documentation.pdf). It perfectly details the available endpoints, parameter requirements, and expected JSON responses.