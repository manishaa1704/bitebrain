# BiteBrain API - Presentation Outline (10 Mins)

## 0:00 - 1:00 | Introduction & Project Concept
- **Greeting**: Introduce yourself and the "BiteBrain API". 
- **Concept**: Briefly explain that BiteBrain is a nutritional intelligence and recipe management API. (Relates to the "Nutrition and recipe analytics API" idea in the brief).
- **Goal**: Highlight what problem it solves: tracking ingredients and calculating precise macronutrients for composite recipes.

## 1:00 - 2:00 | Technical Stack & Architecture
- **Framework**: Explain the choice of Python & FastAPI (mention performance and auto-docs).
- **Database**: Explain the choice of SQLite & SQLAlchemy ORM. Mention that a relational database was chosen because ingredients and recipes have a strict many-to-many relationship (recipes contain multiple ingredients).
- **Version Control**: Briefly display your GitHub commit history (showing consistent version control discipline as required).

## 2:00 - 4:00 | API Demonstration (The Demo)
- **Live Demo (Swagger UI)**: Open `http://localhost:8000/docs`.
- **CRUD Operations**: 
  - *Create*: Show how to create a new Ingredient via POST.
  - *Read*: Show how to list Recipes via GET.
  - *Update*: Show modifying a Recipe's servings via PUT.
  - *Delete*: Show deleting an item via DELETE.
- **Complexity**: Highlight the `/recipes/{recipe_id}/ingredients` endpoint which handles linking ingredients to recipes.

## 4:00 - 5:00 | Testing, Challenges, and Conclusion
- **Testing**: Briefly show your `pytest` suite running in the terminal (`pytest tests/ -v`). State that thorough automated testing ensures the API handles errors correctly (e.g., returning 404 for missing items).
- **GenAI Reflection**: Briefly mention how AI was used productively (e.g., generating tests, debugging complex schema validation).
- **Conclusion**: Thank the examiners and open the floor to Q&A.

---
*(End of Presentation Phase. The next 5 minutes are Q&A.)* 

**Tips for Q&A:**
- Be prepared to discuss *why* you chose FastAPI over Django.
- Be prepared to discuss your database relationship choices (Foreign Keys).
- Be prepared to explain any specific line of code if asked.
