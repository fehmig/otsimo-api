import json
import random

def load_menu_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

menu_data = load_menu_data('data/menu_data.json')

def filter_meals(is_vegetarian, is_vegan):
    for meal in menu_data['meals']:
        if is_vegetarian:
            if not is_meal_vegetarian(meal):
                continue
        if is_vegan:
            if not is_meal_vegan(meal):
                continue
        yield meal

def get_meal(meal_id):
    for meal in menu_data['meals']:
        if meal['id'] == meal_id:
            return meal
    return None

def is_meal_vegetarian(meal):
    for ingredient in meal['ingredients']:
        if not is_ingredient_vegetarian(ingredient):
            return False
    return True

def is_meal_vegan(meal):
    for ingredient in meal['ingredients']:
        if not is_ingredient_vegan(ingredient):
            return False
    return True

def is_ingredient_vegetarian(ingredient):
    for option in menu_data['ingredients']:
        if option['name'] == ingredient['name']:
            return 'vegetarian' in option['groups'] or len(option['groups']) == 0  
    return False

def is_ingredient_vegan(ingredient):
    for option in menu_data['ingredients']:
        if option['name'] == ingredient['name']:
            return 'vegan' in option['groups'] or len(option['groups']) == 0  

def calculate_quality_model(meal_id, ingredient_qualities):
    
    meal = get_meal(meal_id)
    if meal is None:
        return {'error': 'Meal not found'}, 404
    
    total_score = 0
    total_ingredients = len(ingredient_qualities)  
    
    for ingredient_name, ingredient_quality in ingredient_qualities.items():
        
        ingredient_name_lower = ingredient_name.lower()
        
        
        found = False
        for ingredient in meal['ingredients']:
            if ingredient['name'].lower() == ingredient_name_lower:
                found = True
             
                if ingredient_quality == 'low':
                    ingredient_score = 10
                elif ingredient_quality == 'medium':
                    ingredient_score = 20
                else:  
                    ingredient_score = 30
                
                total_score += ingredient_score
                break  
        
       
        if not found:
            error_message = f"Ingredient '{ingredient_name}' not found in meal."
            return {'error': error_message}, 400
    
    
    overall_quality = total_score / total_ingredients if total_ingredients > 0 else 0
    
    return {
        'quality': overall_quality
    }


def calculate_price_model(meal_id, ingredient_qualities):
    
    meal = get_meal(meal_id)
    
    if meal is None:
        return {'error': 'Meal not found'}, 404
    
    total_cost = 0
   
    
    for ingredient in meal['ingredients']:
        ingredient_name = ingredient['name']
        ingredient_quantity = ingredient.get('quantity', 0)  
        
       
        ingredient_quality = ingredient_qualities.get(ingredient_name, 'high')
        
       
        options = [opt for opt in menu_data['ingredients'] if opt['name'] == ingredient_name]
        if not options:
            return {'error': f"No price options found for {ingredient_name}"}, 404
        
       
        selected_option = None
        for option in options[0]['options']:
            if option['quality'] == ingredient_quality:
                selected_option = option
                break
        
        if selected_option is None:
            return {'error': f"No price option found for {ingredient_name} with quality {ingredient_quality}"}, 404
  
        ingredient_price_per_kg = selected_option['price']  
        

        
 
        if ingredient_quality == 'low':
            additional_cost = 0.10 
        elif ingredient_quality == 'medium':
            additional_cost = 0.05 
        else:
            additional_cost = 0  

        ingredient_cost = ingredient_price_per_kg * (ingredient_quantity /1000) + additional_cost 

        
        total_cost += ingredient_cost
      
    return {
        'price': round(total_cost, 2)
    }



def select_random_meal_model(budget=None):
   
    selected_meal = random.choice(menu_data['meals'])
    

    selected_meal_price = calculate_price_model(selected_meal['id'], {})
    

    if budget is not None:
        if selected_meal_price['price'] > budget:
            return {'error': 'Meal exceeds budget'}, 400
    

    selected_meal_quality = calculate_quality_model(selected_meal['id'], {})
    
    return {
        'id': selected_meal['id'],
        'name': selected_meal['name'],
        'price': selected_meal_price['price'],
        'quality_score': selected_meal_quality['quality'],
        'ingredients': [{'name': ingredient['name'], 'quality': 'high'} for ingredient in selected_meal['ingredients']]
    }





