import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rrs_project.settings')
django.setup()

from rrs_app.models import Recipe, Ingredient, RecipeIngredient

recipes_data = [
    {
        'title': 'Poha',
        'slug': 'poha',
        'meal_type': 'breakfast',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'A simple Indian breakfast.',
        'ingredients': {
            'poha': 100,
            'onion': 1,
            'cooking oil': 10,
            'salt': 5,
            'turmeric': 2,
        }
    },
    {
        'title': 'Besan Chilla',
        'slug': 'besan-chilla',
        'meal_type': 'breakfast',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'A quick gram flour pancake.',
        'ingredients': {
            'besan': 100,
            'onion': 1,
            'salt': 5,
            'turmeric': 2,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Jeera Rice',
        'slug': 'jeera-rice',
        'meal_type': 'lunch',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'Rice flavored with cumin.',
        'ingredients': {
            'rice': 100,
            'cumin': 5,
            'salt': 5,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Aloo Fry',
        'slug': 'aloo-fry',
        'meal_type': 'lunch',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'A quick potato dish.',
        'ingredients': {
            'potatoes': 150,
            'cooking oil': 10,
            'salt': 5,
            'turmeric': 2,
            'chili powder': 2,
        }
    },
    {
        'title': 'Moong Dal Khichdi',
        'slug': 'moong-dal-khichdi',
        'meal_type': 'lunch',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'A comforting rice and lentil dish.',
        'ingredients': {
            'rice': 50,
            'moong dal': 50,
            'turmeric': 2,
            'salt': 5,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Dal Tadka',
        'slug': 'dal-tadka',
        'meal_type': 'lunch',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'A simple lentil dish with basic spices.',
        'ingredients': {
            'moong dal': 100,
            'tomato': 1,
            'onion': 1,
            'turmeric': 2,
            'salt': 5,
            'cumin': 5,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Masala Omelette',
        'slug': 'masala-omelette',
        'meal_type': 'breakfast',
        'diet_type': 'non-veg',
        'effort': 'easy',
        'description': 'A quick omelette with onion and spices.',
        'ingredients': {
            'egg': 2,
            'onion': 1,
            'salt': 5,
            'chili powder': 2,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Tomato Rice',
        'slug': 'tomato-rice',
        'meal_type': 'lunch',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'Simple rice cooked with tomato and spices.',
        'ingredients': {
            'rice': 100,
            'tomato': 1,
            'onion': 1,
            'salt': 5,
            'turmeric': 2,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Vegetable Upma',
        'slug': 'vegetable-upma',
        'meal_type': 'breakfast',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'A simple semolina breakfast.',
        'ingredients': {
            'semolina': 100,
            'onion': 1,
            'carrot': 1,
            'salt': 5,
            'turmeric': 2,
            'cooking oil': 10,
        }
    },
    {
        'title': 'Aloo Paratha',
        'slug': 'aloo-paratha',
        'meal_type': 'breakfast',
        'diet_type': 'veg',
        'effort': 'easy',
        'description': 'Indian flatbread stuffed with potatoes.',
        'ingredients': {
            'wheat flour': 100,
            'potatoes': 100,
            'salt': 5,
            'chili powder': 2,
            'cooking oil': 10,
        }
    },
]

for data in recipes_data:
    ingredients = data['ingredients']

    recipe, created = Recipe.objects.get_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'meal_type': data['meal_type'],
            'diet_type': data['diet_type'],
            'effort': data['effort'],
            'description': data['description'],
        }
    )

    for ingredient_title, amount in ingredients.items():
        ingredient = Ingredient.objects.filter(
            title__iexact=ingredient_title
        ).first()

        if ingredient:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={'amount': amount}
            )

print("Indian recipes added successfully!")