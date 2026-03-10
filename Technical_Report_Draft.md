# Technical Report: BiteBrain API

## 1. Introduction and Architecture
The BiteBrain API is a sophisticated RESTful web service designed to manage nutritional ingredients, construct composite recipes, and generate dietary analytics. The architecture follows a multi-tier pattern separating routing (`app/routers`), business logic/services (`app/services`), data access and definition (`app/models`), and data validation constraints (`app/schemas`).

## 2. Technology Stack Justification
**Programming Language: Python**
Python was selected due to its readability, rapid development cycle, and unparalleled ecosystem for backend logic, especially concerning data processing and AI integrations if expanded in the future.

**Framework: FastAPI**
FastAPI was chosen over alternatives like Django or Flask because of its native asynchronous support, automatic interactive documentation (Swagger UI) generation from Pydantic models, and high performance driven by Starlette and Pydantic. It inherently enforces type hints, significantly reducing runtime errors and improving API reliability.

**Database: SQLite & SQLAlchemy (Relational Database)**
A relational database (SQLite accessed via SQLAlchemy ORM) was selected over NoSQL alternatives (like MongoDB) because the core data structure (Users, Ingredients, Recipes, and the many-to-many relationships between them) is highly structured and relational. Ensuring immediate consistency and enforcing foreign key constraints is vital for accurate nutritional tracking. SQLite was chosen for this coursework to ensure an out-of-the-box local execution experience without demanding a secondary database daemon, though the use of SQLAlchemy allows for a seamless transition to PostgreSQL in production.

## 3. Challenges and Testing Approach
**Challenges**: A major complexity involved managing the many-to-many relationship between `Recipe` and `Ingredient` while accurately calculating scaled nutritional metrics based on `quantity_grams`.
**Testing**: A comprehensive test suite was developed using `pytest`. The strategy isolated tests using an in-memory SQLite database (`TestClient`) explicitly resetting states between sessions. Tests were created to robustly verify CRUD operations, edge cases (e.g., retrieving non-existent IDs), and error handling integrity. 

## 4. Limitations and Future Development
Currently, the system assumes static caloric definitions. Future improvements would include:
- Integration with an external public dataset (e.g., USDA FoodData Central) to dynamically fetch and update generic ingredient macronutrients upon creation.
- A functional frontend client using Next.js or React to visualize the meal plan statistics.

## 5. Generative AI Declaration
**Rule Adherence**: This coursework adhered to the Green Light Assessment criteria.
**Usage Level / Tools**: Generative AI (Google Deepmind Assistant and Google Gemini API) was used for high-level tasks to aid creative thinking, debug dependency issues, and rapidly synthesize boilerplate structures. 
**Purposes**: 
1. **Planning & Debugging**: AI was used to parse runtime schema validation errors in `pytest` to pinpoint missing response fields.
2. **Scripting**: AI generated a python script to automatically convert the OpenAPI JSON spec into markdown documentation.
3. **Drafting**: AI assisted in drafting this report structured based on the coursework specifications.
4. **Endpoint Integration**: The `Google Gemini API (gemini-2.5-flash)` was natively integrated into the `/analytics/substitute` endpoint to provide intelligent ingredient substitution functionality gracefully.
