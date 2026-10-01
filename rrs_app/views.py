from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from . import models
from . import forms
from .models import Recipe, Ingredient, RecipeIngredient, UserIngredient, UserInfo
from .forms import SignUpForm, EditProfileForm, MyPasswordChangeForm, UserIngredientForm, RecipeForm
from django.contrib.auth.models import User
import requests
THEMEALDB_API_URL = 'https://www.themealdb.com/api/json/v1/1'

def home(request):
    return render(request, 'rrs_app/home.html', {})


def login_user(request):
    if request.method == 'POST': #if someone fills out form , Post it
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:# if user exist
            login(request, user)
            messages.success(request,('Successfully logged in.'))
            return redirect('home') #routes to 'home' on successful login
        else:
            messages.error(request,('Username or password is wrong!'))
            return redirect('login') #re routes to login page upon unsucessful login
    else:
        return render(request, 'rrs_app/login.html', {})


def logout_user(request):
    logout(request)
    messages.warning(request,('Successfully logged out.'))
    return redirect('home')


def register_user(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ('Successfully registered.'))
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'rrs_app/register.html', context)


def edit_profile(request):
    if request.method =='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('Profile successfully edited.'))
            return redirect('home')
    else:         #passes in user information
        if len(str(request.user)) >= 32:
            form = EditProfileForm()
            messages.error(request, ('Guests cannot edit profile info!'))
            return redirect('input_form')
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'rrs_app/edit_profile.html', context)


def change_password(request):
    if request.method =='POST':
        form = MyPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('Password successfully edited.'))
            return redirect('home')
    else:         #passes in user information
        form = MyPasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'rrs_app/change_password.html', context)


def faq(request):
    return render(request, 'rrs_app/faq.html', {})


def input_form_view(request):
    if not request.user.is_authenticated:
        if not request.session.exists(request.session.session_key):
            request.session.create()

        username = request.session.session_key

        try:
            user = User.objects.create_user(
                username=username,
                email=username + '@anonymous.com',
                password=username
            )
        except:
            user = User.objects.get(username=username)

        login(request, user)
        messages.warning(request, 'Proceeding with a guest user.')

    # Create default user information
    UserInfo.objects.get_or_create(
        user=request.user,
        defaults={
            'addcost': 1000000,
            'portion': 1
        }
    )

    return redirect('pantry_create')

def useringredient_form_view(request):
    form = forms.UserIngredientForm()

    if not request.user.is_authenticated:
        messages.warning(request, 'Redirecting to the home page!')
        return redirect('home')

    ingredient_list = UserIngredient.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        # DELETE ingredient
        if 'remove' in request.POST:
            ingredient_id = request.POST.get('remove_id')

            UserIngredient.objects.filter(
                id=ingredient_id,
                user=request.user
            ).delete()

            messages.success(
                request,
                'Ingredient removed from your pantry.'
            )

            return redirect('pantry_create')

        # UPDATE ingredient
        if 'update' in request.POST:
            ingredient_id = request.POST.get('update_id')

            try:
                user_ingredient = UserIngredient.objects.get(
                    id=ingredient_id,
                    user=request.user
                )

                form = forms.UserIngredientForm(request.POST)

                if form.is_valid():
                    new_ingredient = form.cleaned_data['ingredient']

                    if new_ingredient is None:
                        messages.warning(
                            request,
                            'Please select an ingredient.'
                        )
                    else:
                        # Prevent duplicate ingredient entries
                        duplicate_exists = UserIngredient.objects.filter(
                            user=request.user,
                            ingredient=new_ingredient
                        ).exclude(
                            id=ingredient_id
                        ).exists()

                        if duplicate_exists:
                            messages.warning(
                                request,
                                'That ingredient is already in your pantry.'
                            )
                        else:
                            user_ingredient.ingredient = new_ingredient
                            user_ingredient.save()

                            messages.success(
                                request,
                                'Ingredient updated successfully.'
                            )

                    return redirect('pantry_create')

            except UserIngredient.DoesNotExist:
                messages.warning(
                    request,
                    'Ingredient not found.'
                )

                return redirect('pantry_create')

        # ADD / COMPLETE
        form = forms.UserIngredientForm(request.POST)

        if form.is_valid():

            ingredient_list = UserIngredient.objects.filter(
                user=request.user
            )

            if 'complete' in request.POST:
                messages.success(
                    request,
                    'Matching recipes are listed below.'
                )
                return redirect('recipe_list')

            if 'add' in request.POST:

                ingredient = form.cleaned_data['ingredient']

                if ingredient is None:
                    messages.warning(
                        request,
                        'Please select an ingredient.'
                    )

                    return render(
                        request,
                        'rrs_app/useringredient_form.html',
                        {
                            'form': form,
                            'ingredient_list': ingredient_list
                        }
                    )

                try:
                    ui = UserIngredient.objects.get(
                        user=request.user,
                        ingredient=ingredient
                    )

                    ui.amount = form.cleaned_data['amount']
                    ui.save()

                    messages.success(
                        request,
                        "The ingredient's amount is successfully updated."
                    )

                except UserIngredient.DoesNotExist:
                    ui = UserIngredient(
                        user=request.user,
                        ingredient=ingredient,
                        amount=form.cleaned_data['amount']
                    )
                    ui.save()

                    messages.success(
                        request,
                        'The ingredient is successfully added to your pantry.'
                    )

                form = forms.UserIngredientForm()

                ingredient_list = UserIngredient.objects.filter(
                    user=request.user
                )

                return render(
                    request,
                    'rrs_app/useringredient_form.html',
                    {
                        'form': form,
                        'ingredient_list': ingredient_list
                    }
                )

        else:
            messages.warning(
                request,
                'Please select a valid ingredient.'
            )

            return render(
                request,
                'rrs_app/useringredient_form.html',
                {
                    'form': form,
                    'ingredient_list': ingredient_list
                }
            )

    return render(
        request,
        'rrs_app/useringredient_form.html',
        {
            'form': form,
            'ingredient_list': ingredient_list
        }
    )


def recipe_form_view(request):
    form = forms.RecipeForm()

    if not request.user.is_authenticated:
        messages.warning(request, 'Redirecting to the home page!')
        return redirect('home')

    recipe_list = []

    for rec in Recipe.objects.all():
        total_ingredients = RecipeIngredient.objects.filter(
            recipe=rec
        ).count()

        matched_ingredients = 0
        missing_ingredients = []

        for rec_item in RecipeIngredient.objects.filter(recipe=rec):
            ing = Ingredient.objects.get(title=rec_item.ingredient)

            # Check whether the user has the ingredient
            user_has_ingredient = UserIngredient.objects.filter(
                user=request.user,
                ingredient=rec_item.ingredient
            ).exists()

            if user_has_ingredient:
                matched_ingredients += 1
                continue

            # Check whether the user has a substitute
            substitute_found = False

            if ing.substitutes:
                substitute_names = [
                    name.strip()
                    for name in ing.substitutes.split(',')
                ]

                for substitute_name in substitute_names:
                    substitute = Ingredient.objects.filter(
                        title__iexact=substitute_name
                    ).first()

                    if substitute:
                        has_substitute = UserIngredient.objects.filter(
                            user=request.user,
                            ingredient=substitute
                        ).exists()

                        if has_substitute:
                            matched_ingredients += 1
                            substitute_found = True
                            break

            if not substitute_found:
                missing_ingredients.append(ing.title)

        # Calculate match percentage
        if total_ingredients > 0:
            rec.match_percentage = round(
                (matched_ingredients / total_ingredients) * 100,
                1
            )
        else:
            rec.match_percentage = 0

        # Store missing ingredients for the template
        rec.missing_ingredients = missing_ingredients

        # No quantity-based cost calculation
        rec.total_cost = 0

        recipe_list.append(rec)

    # Show recipes with the highest matching ingredients first
    recipe_list.sort(
        key=lambda x: x.match_percentage,
        reverse=True
    )

    if request.method == 'POST':
        form = forms.RecipeForm(request.POST)

        if form.is_valid():
            if 'filter' in request.POST:
                if form.cleaned_data['meal_type'] is not None:
                    recipe_list = [
                        recipe for recipe in recipe_list
                        if recipe.meal_type == form.cleaned_data['meal_type']
                    ]

                if form.cleaned_data['diet_type'] is not None:
                    recipe_list = [
                        recipe for recipe in recipe_list
                        if recipe.diet_type == form.cleaned_data['diet_type']
                    ]

                if form.cleaned_data['effort'] is not None:
                    recipe_list = [
                        recipe for recipe in recipe_list
                        if recipe.effort == form.cleaned_data['effort']
                    ]

            elif 'reset' in request.POST:
                form = forms.RecipeForm()

    return render(
        request,
        'rrs_app/recipe_list.html',
        {'form': form, 'recipe_list': recipe_list}
    )
def recipe_detail_view(request, slug):

    if not request.user.is_authenticated:
        messages.warning(request, 'Redirecting to the home page!')
        return redirect('home')

    rec = Recipe.objects.get(slug=slug)
    inf = UserInfo.objects.get(user=request.user)
    recipe_list = []
    ingredient_list = []

    for rec_item in RecipeIngredient.objects.filter(recipe=rec):
        ing = Ingredient.objects.get(title=rec_item.ingredient)
        recipe_list.append(rec_item)

        try:
            user_item = UserIngredient.objects.get(
                user=request.user,
                ingredient=rec_item.ingredient
            )

            amount_diff = rec_item.amount * inf.portion - user_item.amount
            user_item.substitute_suggestions = []

            if ing.substitutes:
                user_item.substitute_suggestions = [
                    name.strip()
                    for name in ing.substitutes.split(',')
                ]

            if amount_diff > 0:
                user_item.amount = amount_diff

                if ing.unit_type != 'count':
                    user_item.total_cost = (
                        ing.unit_cost * user_item.amount / 1000
                    )
                else:
                    user_item.total_cost = (
                        ing.unit_cost * user_item.amount
                    )

            else:
                user_item.amount = "-"
                user_item.total_cost = "-"


            ingredient_list.append(user_item)

        except UserIngredient.DoesNotExist:
            rec_item.amount = rec_item.amount * inf.portion

            if ing.unit_type != 'count':
                rec_item.total_cost = (
                    ing.unit_cost * rec_item.amount / 1000
                )
            else:
                rec_item.total_cost = (
                    ing.unit_cost * rec_item.amount
                )

            rec_item.substitute_suggestions = []

            if ing.substitutes:
                rec_item.substitute_suggestions = [
                    name.strip()
                    for name in ing.substitutes.split(',')
                ]
            ingredient_list.append(rec_item)

    ingredient_list = list(zip(recipe_list, ingredient_list))

    if 'completed' in request.POST and request.POST.getlist("check") == ['on']:

        for rec_item in RecipeIngredient.objects.filter(recipe=rec):
            ing = Ingredient.objects.get(title=rec_item.ingredient)

            try:
                user_item = UserIngredient.objects.get(
                    user=request.user,
                    ingredient=rec_item.ingredient
                )

                amount_diff = rec_item.amount * inf.portion - user_item.amount

                if amount_diff > 0:
                    user_item.amount = 0
                    user_item.save()

                else:
                    user_item.amount = (
                        user_item.amount - rec_item.amount * inf.portion
                    )
                    user_item.save()

            except UserIngredient.DoesNotExist:
                pass

        messages.warning(
            request,
            'Given amounts of the ingredients are subtracted from your pantry!'
        )

        return redirect('recipe_detail', slug=slug)

    return render(
        request,
        'rrs_app/recipe_detail.html',
        {
            'recipe_details': rec,
            'ingredient_list': ingredient_list
        }
    )

def online_recipe_search(request):
    meals = []
    search_query = ""
    error_message = ""

    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to explore online recipes.')
        return redirect('login')

    if request.method == 'POST':
        search_query = request.POST.get('search', '').strip()

        if search_query:
            try:
                response = requests.get(
                    f'{THEMEALDB_API_URL}/search.php',
                    params={'s': search_query},
                    timeout=10
                )

                response.raise_for_status()

                data = response.json()
                meals = data.get('meals') or []

            except requests.RequestException:
                error_message = (
                    'Unable to connect to the online recipe service. '
                    'Please try again later.'
                )

    return render(
        request,
        'rrs_app/online_recipe_search.html',
        {
            'meals': meals,
            'search_query': search_query,
            'error_message': error_message,
        }
    )

def online_recipe_detail(request, meal_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to explore online recipes.')
        return redirect('login')

    meal = None
    error_message = ""

    try:
        response = requests.get(
            f'{THEMEALDB_API_URL}/lookup.php',
            params={'i': meal_id},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        meals = data.get('meals') or []

        if meals:
            meal = meals[0]
        else:
            error_message = 'Recipe not found.'

    except requests.RequestException:
        error_message = (
            'Unable to connect to the online recipe service. '
            'Please try again later.'
        )

    return render(
        request,
        'rrs_app/online_recipe_detail.html',
        {
            'meal': meal,
            'error_message': error_message,
        }
    )