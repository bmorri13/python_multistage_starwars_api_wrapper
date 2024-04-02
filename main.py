from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_swapi_url(endpoint, search_term):
    swapi_url = f'https://swapi.dev/api/{endpoint}/'
    if search_term:
        swapi_url += f'?search={search_term}'

    response = requests.get(swapi_url)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch data from SWAPI"}, response.status_code

@app.route('/ships', methods=['GET'])
def get_starships():
    search_term = request.args.get('search', None)
    response, status = get_swapi_url("starships", search_term)
    return jsonify(response), status

@app.route('/characters', methods=['GET'])
def get_people():
    search_term = request.args.get('search', None)
    response, status = get_swapi_url("people", search_term)
    return jsonify(response), status

@app.route('/', defaults={'path': ''})
@app.route('/')
def home():
    api_list = {
        "_welcome_note": "Star Wars APi Wrapper from SWAPI. Use the available APIs to access information about Star Wars starships and characters.",
        "available_apis": {
            "/ships": "Access information about Star Wars starships. Use the 'search' query parameter to filter results.",
            "/characters": "Access information about Star Wars characters. Use the 'search' query parameter to filter results.",
            "/": "Home page listing all available APIs.",
        "search_query": "Use the 'search' query parameter to filter results based on the name of the starship or character."
        }
    }
    return jsonify(api_list)

@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Not active API"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)