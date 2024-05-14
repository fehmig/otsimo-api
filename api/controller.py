from .model import get_meal, filter_meals, calculate_quality_model, calculate_price_model,select_random_meal_model, menu_data

def list_meals(is_vegetarian, is_vegan):
    return list(filter_meals(is_vegetarian, is_vegan))

def get_meal_by_id(meal_id):
    return get_meal(meal_id)

def calculate_quality_controller(meal_id, ingredient_qualities):
    
    if not meal_id:
        return {'error': 'Meal ID is required'}, 400

    
    quality_result = calculate_quality_model(meal_id, ingredient_qualities)
    
    if quality_result is not None:
        return {'quality': quality_result}, 200
    else:
        return {'error': 'Meal not found'}, 404

def calculate_price_controller(meal_id, ingredient_qualities):
   
    if not meal_id:
        return {'error': 'Meal ID is required'}, 400

   
    price_result = calculate_price_model(meal_id, ingredient_qualities)
    
    if price_result is not None:
        return {'price': price_result}, 200
    else:
        return {'error': 'Meal not found'}, 404
    

def select_random_meal_controller(budget=None):
    return select_random_meal_model(budget)

def search_meal_controller(query):
    matched_meals = []
    for meal in menu_data['meals']:
        if query.lower() in meal['name'].lower():
            matched_meals.append({
                'id': meal['id'],
                'name': meal['name'],
                'ingredients': [ingredient for ingredient in meal['ingredients']]
            })
    return matched_meals
