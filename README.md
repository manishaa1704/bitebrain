# BiteBrain API

BiteBrain is a high-performance, AI-integrated nutrition intelligence API. It provides a robust platform for managing personal nutrition, recipes, and meal planning, enhanced by real-world data integration and cutting-edge Model Context Protocol (MCP) support.

##  Live API
- **Base URL**: https://bitebrain.onrender.com
- **Swagger UI**: https://bitebrain.onrender.com/docs
- **ReDoc**: https://bitebrain.onrender.com/redoc

Developed as part of the **COMP3011 Web Services API Development** coursework at the University of Leeds.

##  Key Features

- **Smart Ingredient Management**: CRUD operations for ingredients with automatic nutritional data fetching via the **OpenFoodFacts API**.
- **Dynamic Recipe Engine**: Build complex recipes from multiple ingredients with automatic total macro and cost calculation.
- **AI-Powered Substitutions**: Integrated **Google Gemini Pro** engine to suggest intelligent ingredient alternatives based on dietary needs (e.g., "Make it vegan" or "Lower calorie").
- **Meal Planning**: personalized weekly meal plans with total nutritional summaries.
- **AI-Native Integration**: Fully compatible **MCP Server** implementation for seamless interaction with AI assistants (Claude, Cursor, etc.).
- **Professional Deployment**: Containerized with **Docker** and **Docker Compose** for consistent environment behavior.

##  Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **Database**: SQLite with SQLAlchemy ORM
- **AI Engine**: Google Gemini (via `google-generativeai`)
- **Data Integration**: OpenFoodFacts API
- **Deployment**: Docker / Docker Compose
- **Testing**: Pytest with automated test suite

##  Setup Instructions

### 1. Prerequisites
- Python 3.12+
- Docker (optional, for containerized run)
- A Google Gemini API Key

### 2. Manual Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/manishaa1704/bitebrain.git
   cd bitebrain
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///./bitebrain.db
   SECRET_KEY=your_super_secret_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 3. Docker Installation
```bash
docker compose up --build
```

##  Testing
The project includes a comprehensive test suite (17+ tests) covering all core logic.
```bash
PYTHONPATH=. pytest tests/ -v
```

##  Model Context Protocol (MCP)
To run the BiteBrain MCP server for use with AI assistants:
```bash
PYTHONPATH=. python app/mcp_server.py
```

##  Documentation
- **Technical Report**: [Technical_Report.pdf](./Technical_Report.pdf) (Contains design justification and GenAI declaration)
- **API Reference**: [API_Documentation.pdf](./API_Documentation.pdf) (Detailed endpoint schema and examples)
- **Presentation Outline**: [Presentation_Outline.md](./Presentation_Outline.md)
