# BiteBrain API API Documentation

**Version**: 1.0.0
**Description**: A smart recipe and nutrition intelligence API

## `POST /auth/register`

**Summary**: Register

Register a new user

### Request Body
Expects a JSON body corresponding to the `UserCreate` schema.

### Responses
| Status Code | Description |
|---|---|
| 201 | Successful Response |
| 422 | Validation Error |

---

## `POST /auth/login`

**Summary**: Login

Login and receive a JWT token

### Request Body
### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `GET /ingredients/`

**Summary**: Get All Ingredients

Get all ingredients with pagination

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| skip | query | No | integer |
| limit | query | No | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `POST /ingredients/`

**Summary**: Create Ingredient

Create a new ingredient (requires authentication)

### Request Body
Expects a JSON body corresponding to the `IngredientCreate` schema.

### Responses
| Status Code | Description |
|---|---|
| 201 | Successful Response |
| 422 | Validation Error |

---

## `GET /ingredients/{ingredient_id}`

**Summary**: Get Ingredient

Get a single ingredient by ID

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| ingredient_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `PUT /ingredients/{ingredient_id}`

**Summary**: Update Ingredient

Update an ingredient (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| ingredient_id | path | Yes | integer |

### Request Body
Expects a JSON body corresponding to the `IngredientUpdate` schema.

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `DELETE /ingredients/{ingredient_id}`

**Summary**: Delete Ingredient

Delete an ingredient (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| ingredient_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 204 | Successful Response |
| 422 | Validation Error |

---

## `GET /recipes/`

**Summary**: Get All Recipes

Get all recipes

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| skip | query | No | integer |
| limit | query | No | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `POST /recipes/`

**Summary**: Create Recipe

Create a new recipe with ingredients (requires authentication)

### Request Body
Expects a JSON body corresponding to the `RecipeCreate` schema.

### Responses
| Status Code | Description |
|---|---|
| 201 | Successful Response |
| 422 | Validation Error |

---

## `GET /recipes/{recipe_id}`

**Summary**: Get Recipe

Get a single recipe by ID

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `PUT /recipes/{recipe_id}`

**Summary**: Update Recipe

Update a recipe (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Request Body
Expects a JSON body corresponding to the `RecipeUpdate` schema.

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `DELETE /recipes/{recipe_id}`

**Summary**: Delete Recipe

Delete a recipe (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 204 | Successful Response |
| 422 | Validation Error |

---

## `POST /recipes/{recipe_id}/ingredients`

**Summary**: Add Ingredient To Recipe

Add an ingredient to an existing recipe (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Request Body
Expects a JSON body corresponding to the `RecipeIngredientAdd` schema.

### Responses
| Status Code | Description |
|---|---|
| 201 | Successful Response |
| 422 | Validation Error |

---

## `GET /meal-plans/`

**Summary**: Get My Meal Plans

Get all meal plans for the current user

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |

---

## `POST /meal-plans/`

**Summary**: Create Meal Plan

Create a new meal plan (requires authentication)

### Request Body
Expects a JSON body corresponding to the `MealPlanCreate` schema.

### Responses
| Status Code | Description |
|---|---|
| 201 | Successful Response |
| 422 | Validation Error |

---

## `GET /meal-plans/{meal_plan_id}`

**Summary**: Get Meal Plan

Get a single meal plan by ID

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| meal_plan_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `PUT /meal-plans/{meal_plan_id}`

**Summary**: Update Meal Plan

Update a meal plan (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| meal_plan_id | path | Yes | integer |

### Request Body
Expects a JSON body corresponding to the `MealPlanUpdate` schema.

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `DELETE /meal-plans/{meal_plan_id}`

**Summary**: Delete Meal Plan

Delete a meal plan (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| meal_plan_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 204 | Successful Response |
| 422 | Validation Error |

---

## `POST /meal-plans/{meal_plan_id}/recipes`

**Summary**: Add Recipe To Meal Plan

Add a recipe to a meal plan (requires authentication)

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| meal_plan_id | path | Yes | integer |

### Request Body
Expects a JSON body corresponding to the `MealPlanRecipeAdd` schema.

### Responses
| Status Code | Description |
|---|---|
| 201 | Successful Response |
| 422 | Validation Error |

---

## `GET /analytics/recipe/{recipe_id}/macros`

**Summary**: Get Recipe Macros

Get full macro breakdown for a recipe.
Returns calories, protein, carbs and fat both total and per serving.

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `GET /analytics/recipe/{recipe_id}/allergens`

**Summary**: Get Allergens

Get allergen warnings for a recipe.
Also returns vegetarian and vegan status.

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `GET /analytics/recipe/{recipe_id}/cost`

**Summary**: Get Recipe Cost

Get estimated cost breakdown for a recipe.

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| recipe_id | path | Yes | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `GET /analytics/trends/popular-ingredients`

**Summary**: Popular Ingredients

Get the most frequently used ingredients across all recipes.

### Parameters
| Name | In | Required | Type |
|---|---|---|---|
| limit | query | No | integer |

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `GET /analytics/summary`

**Summary**: Nutrition Summary

Get a high level summary of all nutrition data in the system.

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |

---

## `POST /analytics/substitute`

**Summary**: Substitute Ingredient

AI-powered ingredient substitution suggestions.
Uses Claude AI to suggest the best substitutes based on your reason
(e.g. vegan, allergy, lower calories, cheaper).
Requires authentication.

### Request Body
Expects a JSON body corresponding to the `SubstitutionRequest` schema.

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |
| 422 | Validation Error |

---

## `GET /`

**Summary**: Root

### Responses
| Status Code | Description |
|---|---|
| 200 | Successful Response |

---

## Data Schemas

### Body_login_auth_login_post
| Property | Type | Required | Default |
|---|---|---|---|
| grant_type | string or null | No | None |
| username | string | Yes | None |
| password | string | Yes | None |
| scope | string | No |  |
| client_id | string or null | No | None |
| client_secret | string or null | No | None |

### HTTPValidationError
| Property | Type | Required | Default |
|---|---|---|---|
| detail | array | No | None |

### IngredientCreate
| Property | Type | Required | Default |
|---|---|---|---|
| name | string | Yes | None |
| calories_per_100g | number or null | No | None |
| protein_per_100g | number or null | No | None |
| carbs_per_100g | number or null | No | None |
| fat_per_100g | number or null | No | None |
| cost_per_100g | number or null | No | None |
| is_vegetarian | boolean | No | True |
| is_vegan | boolean | No | False |
| allergens | string or null | No | None |

### IngredientResponse
| Property | Type | Required | Default |
|---|---|---|---|
| id | integer | Yes | None |
| name | string | Yes | None |
| calories_per_100g | number | Yes | None |
| protein_per_100g | number | Yes | None |
| carbs_per_100g | number | Yes | None |
| fat_per_100g | number | Yes | None |
| cost_per_100g | number or null | Yes | None |
| is_vegetarian | boolean | Yes | None |
| is_vegan | boolean | Yes | None |
| allergens | string or null | Yes | None |

### IngredientUpdate
| Property | Type | Required | Default |
|---|---|---|---|
| name | string or null | No | None |
| calories_per_100g | number or null | No | None |
| protein_per_100g | number or null | No | None |
| carbs_per_100g | number or null | No | None |
| fat_per_100g | number or null | No | None |
| cost_per_100g | number or null | No | None |
| is_vegetarian | boolean or null | No | None |
| is_vegan | boolean or null | No | None |
| allergens | string or null | No | None |

### MealPlanCreate
| Property | Type | Required | Default |
|---|---|---|---|
| name | string | Yes | None |
| description | string or null | No | None |

### MealPlanRecipeAdd
| Property | Type | Required | Default |
|---|---|---|---|
| recipe_id | integer | Yes | None |
| day_of_week | string or null | No | None |
| meal_type | string or null | No | None |

### MealPlanRecipeResponse
| Property | Type | Required | Default |
|---|---|---|---|
| id | integer | Yes | None |
| recipe_id | integer | Yes | None |
| day_of_week | string or null | Yes | None |
| meal_type | string or null | Yes | None |

### MealPlanResponse
| Property | Type | Required | Default |
|---|---|---|---|
| id | integer | Yes | None |
| name | string | Yes | None |
| description | string or null | Yes | None |
| owner_id | integer | Yes | None |
| recipes | array | No | [] |

### MealPlanUpdate
| Property | Type | Required | Default |
|---|---|---|---|
| name | string or null | No | None |
| description | string or null | No | None |

### RecipeCreate
| Property | Type | Required | Default |
|---|---|---|---|
| name | string | Yes | None |
| description | string or null | No | None |
| instructions | string or null | No | None |
| servings | integer | No | 1 |
| ingredients | array | No | [] |

### RecipeIngredientAdd
| Property | Type | Required | Default |
|---|---|---|---|
| ingredient_id | integer | Yes | None |
| quantity_grams | number | Yes | None |

### RecipeIngredientResponse
| Property | Type | Required | Default |
|---|---|---|---|
| id | integer | Yes | None |
| ingredient_id | integer | Yes | None |
| quantity_grams | number | Yes | None |
| ingredient | any | Yes | None |

### RecipeResponse
| Property | Type | Required | Default |
|---|---|---|---|
| id | integer | Yes | None |
| name | string | Yes | None |
| description | string or null | Yes | None |
| instructions | string or null | Yes | None |
| servings | integer | Yes | None |
| ingredients | array | No | [] |

### RecipeUpdate
| Property | Type | Required | Default |
|---|---|---|---|
| name | string or null | No | None |
| description | string or null | No | None |
| instructions | string or null | No | None |
| servings | integer or null | No | None |

### SubstitutionRequest
| Property | Type | Required | Default |
|---|---|---|---|
| ingredient_name | string | Yes | None |
| reason | string | Yes | None |
| recipe_context | string or null | No | general cooking |

### Token
| Property | Type | Required | Default |
|---|---|---|---|
| access_token | string | Yes | None |
| token_type | string | Yes | None |

### UserCreate
| Property | Type | Required | Default |
|---|---|---|---|
| username | string | Yes | None |
| email | string | Yes | None |
| password | string | Yes | None |

### UserResponse
| Property | Type | Required | Default |
|---|---|---|---|
| id | integer | Yes | None |
| username | string | Yes | None |
| email | string | Yes | None |
| created_at | string | Yes | None |

### ValidationError
| Property | Type | Required | Default |
|---|---|---|---|
| loc | array | Yes | None |
| msg | string | Yes | None |
| type | string | Yes | None |
| input | any | No | None |
| ctx | object | No | None |

