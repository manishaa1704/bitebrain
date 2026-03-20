# Technical Report: BiteBrain API
**Module**: COMP3011 Web Services and Web Data  
**Student**: Manishaa Manickavasagam

**Live API**: https://bitebrain.onrender.com  
**GitHub**: https://github.com/manishaa1704/bitebrain  

---

## 1. Introduction

BiteBrain is a fully-featured, AI-enhanced RESTful web API designed 
for intelligent nutrition management, recipe construction, and 
personalised meal planning. The system goes beyond basic CRUD 
functionality by integrating real-world nutritional data sourcing, 
LLM-powered ingredient substitution, and native Model Context Protocol 
(MCP) support — enabling seamless interaction with modern AI assistants.

The project was developed using an iterative, commit-driven workflow 
across 10 days, reflecting real-world software engineering practice. 
All design decisions were made with scalability, modularity, and 
examiner-facing clarity in mind.

---

## 2. System Architecture

BiteBrain follows a clean, layered architecture that separates concerns
across four distinct layers:

- **Routing Layer**: FastAPI routers (`/auth`, `/ingredients`, 
`/recipes`, `/meal-plans`, `/analytics`) handle HTTP requests and 
dependency injection via FastAPI's `Depends()` system.
- **Service Layer**: Business logic is isolated in `app/services/`, 
separating nutrition calculations and AI substitution logic from 
routing concerns.
- **Data Layer**: SQLAlchemy ORM models define the relational schema 
with strict foreign key constraints and relationship mappings.
- **Validation Layer**: Pydantic V2 schemas enforce strict data typing 
on all inputs and outputs, and power the auto-generated Swagger UI 
documentation.

### Database Schema

The database uses four primary tables with two junction tables to 
handle many-to-many relationships:
```
Users ──< MealPlans ──< MealPlanRecipes >── Recipes
                                               │
                                        RecipeIngredients
                                               │
                                          Ingredients
```

The `RecipeIngredient` junction table carries `quantity_grams` — data 
that belongs to the relationship itself rather than either entity. 
Similarly, `MealPlanRecipe` stores `day_of_week` and `meal_type`. 
This design avoids data redundancy and maintains referential integrity 
through foreign key constraints enforced at the database level.

All nutrition data is stored per 100g, following the international 
food labelling standard. This makes macro calculations straightforward: 
`actual_value = (quantity_grams / 100) * value_per_100g`.

---

## 3. Technology Stack Justification

### Python + FastAPI
FastAPI was chosen over Django REST Framework for several reasons. 
FastAPI natively supports asynchronous request handling, provides 
automatic OpenAPI/Swagger documentation with zero configuration, and 
has best-in-class support for modern Python type hints via Pydantic. 
Its performance benchmarks consistently outperform Django for API 
workloads. The rapid development cycle was also critical given the 
project timeline.

### SQLite + SQLAlchemy ORM
SQLite was selected for its zero-configuration setup during development,
while SQLAlchemy's ORM abstraction means migrating to PostgreSQL for 
production requires only a single environment variable change — no 
code modifications. The relational model was essential for this project 
given the many-to-many relationships between recipes and ingredients. 
A NoSQL database such as MongoDB was considered but rejected because 
the structured, relational nature of nutritional data (ingredients 
belonging to multiple recipes with specific quantities) is better 
served by a relational schema with enforced constraints.

### JWT Authentication
JSON Web Tokens were chosen for stateless authentication. Unlike 
session-based authentication, JWT requires no server-side session 
storage, making the API horizontally scalable. Passwords are hashed 
using bcrypt before storage — plain text passwords are never persisted.

### Google Gemini 2.0 Flash
The Gemini API was integrated for the AI ingredient substitution 
endpoint. Rather than maintaining a static substitution lookup table, 
Gemini reasons about culinary context, dietary restrictions, and 
nutritional impact dynamically. The newer `google-genai` SDK was 
deliberately chosen over the deprecated `google-generativeai` package 
to ensure long-term maintainability.

### Docker
Docker containerisation ensures consistent behaviour across development,
testing, and production environments. The included `Dockerfile` and 
`docker-compose.yml` allow any developer to run BiteBrain with a 
single command: `docker compose up --build`.

---

## 4. Advanced Features and Innovation

### Autonomous Data Sourcing (OpenFoodFacts)
A key innovation is the automatic nutritional data enrichment feature. 
When creating an ingredient, users may omit macro values. The API 
detects missing fields and queries the OpenFoodFacts public database 
(world.openfoodfacts.org) in real time, retrieving calories, protein, 
carbohydrates, fat, and allergen information automatically. This 
transforms BiteBrain from a simple data entry tool into an intelligent 
nutritional assistant. The integration handles unit conversion 
(kJ to kcal), data validation, and graceful fallback if the external 
API is unavailable.

### Model Context Protocol (MCP) Server
BiteBrain implements a native MCP server (`app/mcp_server.py`) using 
the official `mcp` Python SDK. This exposes BiteBrain's core 
functionality as native tools for AI assistants such as Claude Desktop 
and Cursor. This represents a genuinely cutting-edge integration — MCP 
was introduced by Anthropic in late 2024 and represents an emerging 
standard for AI-to-API communication. The implementation positions 
BiteBrain as an AI-native API rather than merely an API with AI 
features.

### AI-Powered Ingredient Substitution
The `/analytics/substitute` endpoint accepts an ingredient name, a 
substitution reason (e.g. "vegan", "nut allergy", "lower calories"), 
and recipe context. It passes the full list of available database 
ingredients along with the request to Gemini, which reasons about 
culinary suitability, nutritional impact, and cooking adjustments. 
This goes far beyond traditional rule-based substitution tables.

### Analytics Engine
Four dedicated analytics endpoints provide genuine nutritional 
intelligence: macro breakdowns per serving, allergen detection across 
recipe ingredients, cost estimation, and ingredient popularity trends 
across all recipes. These are computed dynamically from the relational 
database using SQLAlchemy aggregate queries.

---

## 5. Testing Approach

A comprehensive suite of 17 automated tests was developed using 
`pytest` and FastAPI's `TestClient`. The testing strategy covers three 
areas:

**Functional Testing**: Full CRUD lifecycle tests for ingredients, 
recipes, and analytics endpoints verify that create, read, update, and 
delete operations behave correctly under normal conditions.

**Edge Case Testing**: Tests verify correct HTTP status codes for 
missing resources (404), duplicate entries (400), and unauthorised 
access (401), ensuring the API handles invalid inputs gracefully 
rather than returning unhandled exceptions.

**Mocking Strategy**: The Gemini AI client and OpenFoodFacts API are 
mocked using Python's `unittest.mock` library. This ensures tests run 
in under one second without network calls, while still verifying that 
the integration logic correctly processes API responses.

The test suite runs with zero warnings after migrating from deprecated 
library versions (Pydantic V1 `class Config`, SQLAlchemy 1.x 
`declarative_base`, and `google-generativeai`).

---

## 6. Challenges and Lessons Learned

**Dependency Compatibility**: The most significant technical challenge 
was a compatibility conflict between `passlib` and newer versions of 
`bcrypt`, which prevented password hashing from functioning. This was 
resolved by replacing `passlib` entirely with direct `bcrypt` library 
calls, resulting in simpler and more maintainable code. This experience 
reinforced the importance of pinning dependency versions in 
`requirements.txt`.

**Deprecated Libraries**: During development, the `google-generativeai` 
library was officially deprecated. Migrating to the new `google-genai` 
SDK required updating import patterns, client initialisation, and all 
associated test mocks. This highlighted the importance of monitoring 
library maintenance status before adoption.

**OAuth2 Form Compatibility**: FastAPI's `OAuth2PasswordBearer` scheme 
requires form-encoded login data rather than JSON, which required 
updating the login endpoint to use `OAuth2PasswordRequestForm`. This 
was an important lesson in understanding the difference between API 
authentication standards.

**Database Portability**: Ensuring the SQLAlchemy configuration worked 
correctly for both local SQLite development and potential PostgreSQL 
production deployment required careful management of connection 
arguments, particularly the `check_same_thread` parameter which is 
SQLite-specific.

---

## 7. Limitations and Future Development

**Database**: SQLite is not suitable for concurrent production traffic. 
Migrating to PostgreSQL on a managed service such as Supabase or 
Railway would be the immediate next step for production deployment.

**MCP Server Scope**: The current MCP implementation is read-only. 
Future development would expose write operations (creating ingredients 
and recipes) as MCP tools, enabling AI assistants to fully manage 
nutritional data.

**Caching**: OpenFoodFacts API lookups add latency to ingredient 
creation. Implementing Redis caching for frequently requested 
ingredients would significantly improve response times.

**Frontend**: BiteBrain currently has no user interface beyond Swagger 
UI. A React or Next.js dashboard displaying nutritional analytics 
visually would greatly improve accessibility.

**Rate Limiting**: The API currently has no rate limiting on endpoints. 
Implementing rate limiting using `slowapi` would prevent abuse of the 
AI substitution endpoint, which incurs Gemini API costs per request.

---

## 8. Generative AI Declaration

**Usage Level**: Creative Application of Generative AI (90-100 band)

This project used Generative AI at multiple levels throughout 
development, as detailed below:

**Architecture and Design**: Claude (Anthropic) was used to explore 
high-level architectural alternatives — for example, evaluating 
FastAPI vs Django REST Framework, assessing whether a NoSQL or 
relational database was more appropriate, and designing the junction 
table schema for many-to-many relationships. This constitutes 
high-level AI usage for creative thinking and solution exploration.

**Implementation**: AI assisted with generating boilerplate code for 
CRUD endpoints, Alembic migration configuration, and JWT 
authentication setup. All generated code was reviewed, understood, 
and adapted by the developer.

**Debugging**: AI was used to diagnose the `passlib`/`bcrypt` 
compatibility issue, identify the cause of Pydantic V2 deprecation 
warnings, and resolve the SQLAlchemy `declarative_base` import change.

**Feature Innovation**: The decision to integrate MCP support was 
suggested through AI-assisted research into cutting-edge API standards. 
The AI helped identify MCP as an emerging standard and provided 
guidance on the `mcp` Python SDK.

**Documentation**: AI assisted in structuring the README, generating 
docstrings, and synthesising this technical report.

**Tools Used**: Claude (Anthropic), Google Gemini  
**Conversation Logs**: Exported conversation logs are included as 
Appendix A of this report.

---

## 9. References

- FastAPI Documentation. Sebastián Ramírez. https://fastapi.tiangolo.com/
- SQLAlchemy 2.0 Documentation. https://docs.sqlalchemy.org/
- OpenFoodFacts API. Open Food Facts. https://world.openfoodfacts.org/
- Model Context Protocol Specification. Anthropic, 2024. 
https://modelcontextprotocol.io/
- Google Gemini API Documentation. Google. 
https://ai.google.dev/gemini-api/docs
- Pydantic V2 Migration Guide. https://docs.pydantic.dev/latest/
- bcrypt Python Library. https://pypi.org/project/bcrypt/
- JWT.io — JSON Web Token Introduction. https://jwt.io/introduction
- Python Jose Library. https://python-jose.readthedocs.io/
- Alembic Documentation. https://alembic.sqlalchemy.org/

---

*This report was prepared in accordance with the COMP3011 coursework 
requirements. All GenAI usage has been declared above and conversation 
logs are attached as supplementary material.*
