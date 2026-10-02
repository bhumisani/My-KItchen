# My Kitchen — Ingredient-Aware Recipe Recommendation System

My Kitchen is an enhanced Django-based recipe recommendation system that helps users discover recipes based on the ingredients available in their pantry.

The application compares a user's available ingredients with recipe requirements, identifies missing ingredients, and suggests possible substitutes when available. It also provides recipe filtering, pantry management, authentication, live recipe search, and online recipe discovery through the TheMealDB REST API.

## Project Background

This project is based on the original **Django Recipe Recommendation System**, also known as **Show Me What You Got (SMWYG)**, created by Toyan Ünal.

The original project provided the foundation for recipe recommendations, ingredient management, filtering, authentication, and recipe-related functionality.

This version extends that foundation with additional features and improvements, including:

- Ingredient-based pantry matching
- Missing ingredient identification
- Ingredient substitution suggestions
- Additional Indian ingredients and recipes
- Improved user-specific pantry management
- Database design improvements
- JavaScript-based live recipe search
- Updated responsive user interface
- Online recipe search using the TheMealDB REST API

The original project's license and attribution have been retained.

---

## Features

### User Authentication

- User registration
- User login and logout
- User-specific pantry data
- Protected recipe and pantry functionality

### Pantry Management

Users can manage the ingredients available in their pantry.

- Add ingredients
- Update pantry items
- Remove ingredients
- Maintain a personal ingredient list
- Prevent duplicate ingredients for the same user

### Ingredient-Based Recipe Recommendation

The system compares pantry ingredients with the ingredients required by available recipes.

It can:

- Identify recipes that can be prepared using available ingredients
- Identify missing ingredients
- Match available ingredients through possible substitutions
- Display the ingredients required for each recipe

### Ingredient Substitution

The system provides possible alternatives when a required ingredient is not available.

Examples include:

- Butter → Olive oil
- Milk → Yogurt
- Chicken → Chickpeas
- Onion → Scallion
- Mozzarella → Cheddar cheese
- Mushroom → Aubergine

### Recipe Filtering

Recipes can be filtered based on:

- Meal type
- Diet type
- Effort level

### Live Recipe Search

JavaScript-based live search allows users to search recipes by name without reloading the page.

### Online Recipe Search

The application integrates the **TheMealDB REST API** to allow users to search for additional online recipes.

Users can:

- Search recipes by name
- View recipe images
- View category and cuisine information
- View ingredients and measurements
- View recipe instructions
- Open detailed online recipe information

Recipe data in this section is provided by TheMealDB.

---

## Technologies Used

### Backend

- Python
- Django
- Django ORM
- Requests

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap

### Database

- SQLite

### Python Libraries

- Pillow
- Django-Autoslug
- Requests

### Development Tools

- Visual Studio Code
- PyCharm
- Git
- GitHub

---

## Database Design

The application uses Django's ORM with SQLite.

The main database entities include:

- `User`
- `Ingredient`
- `Recipe`
- `RecipeIngredient`
- `UserIngredient`
- `UserInfo`

Relationships between recipes, ingredients, and users are implemented using Django foreign keys and one-to-one relationships.

Unique constraints are used to prevent duplicate recipe-ingredient and user-ingredient relationships.

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/bhumisani/My-KItchen.git