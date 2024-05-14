from http.server import BaseHTTPRequestHandler, HTTPServer
from api.controller import list_meals, get_meal_by_id, calculate_quality_controller, calculate_price_controller, search_meal_controller, select_random_meal_controller
from urllib.parse import urlparse, parse_qs
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
  

        if parsed_path.path == '/listMeals':
            is_vegetarian = query_params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = query_params.get('is_vegan', ['false'])[0].lower() == 'true'
            meals = list_meals(is_vegetarian, is_vegan)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(meals).encode())

        elif parsed_path.path == '/getMeal':
            meal_id = int(query_params.get('id', [''])[0])
            meal = get_meal_by_id(meal_id)
            if meal:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(meal).encode())
            else:
                self.send_error(404, 'Meal not found')

        elif parsed_path.path == '/search':
            query = query_params.get('query', [''])[0]
            if query:
                matched_meals = search_meal_controller(query)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(matched_meals).encode())
            else:
                self.send_error(400, 'Query parameter is required')        

        else:
            self.send_error(404, 'Endpoint not found')


    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        query_params = parse_qs(post_data)

        if parsed_path.path == '/quality':
            meal_id_param = query_params.get('meal_id')
            if meal_id_param is None or meal_id_param == ['']:
                self.send_error(400, 'Meal ID is missing or empty')
                return
            meal_id = int(meal_id_param[0])
            
            ingredient_qualities = {key: value[0] for key, value in query_params.items() if key != 'meal_id'}
            quality_result = calculate_quality_controller(meal_id, ingredient_qualities)
    
            if quality_result is not None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(quality_result).encode())
            else:
                self.send_error(404, 'Meal not found')

        elif parsed_path.path == '/price':
            meal_id_param = query_params.get('meal_id')
            if meal_id_param is None or meal_id_param == ['']:
                self.send_error(400, 'Meal ID is missing or empty')
                return
            meal_id = int(meal_id_param[0])

            ingredient_qualities = {key: value[0] for key, value in query_params.items() if key != 'meal_id'}
            price_result = calculate_price_controller( meal_id, ingredient_qualities)
            if price_result is not None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(price_result).encode())
            else:
                self.send_error(404, 'Meal not found')

        elif parsed_path.path == '/random':
           
            budget_param = query_params.get('budget')
            if budget_param is not None:
                try:
                    budget = float(budget_param[0])
                except ValueError:
                    self.send_error(400, 'Invalid budget parameter')
                    return
            else:
                budget = None

            
            random_meal = select_random_meal_controller(budget)
            if 'error' in random_meal:
                self.send_error(random_meal.get('status', 500), random_meal['error'])
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(random_meal).encode())
         

        else:
            self.send_error(404, 'Endpoint not found')


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
