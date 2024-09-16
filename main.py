from flask import Flask, Blueprint, request, jsonify
import json
from pydantic import ValidationError
from models.travel_plan_request import TravelPlanRequest
from models.location_request import LocationRequest 
from services import generate_location_data, generate_travel_plan
from places_service import get_lat_lng, nearby_search, get_place_details, fetch_weather_data
from utils.construct_prompt import construct_prompt
from utils.construct_location_prompt import construct_location_prompt 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_route():
    try:
        return jsonify({"travel_plan": "travel_plan"}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/generate-travel-plan', methods=['POST'])
def generate_travel_plan_route():
    try:
        data = TravelPlanRequest(**request.json)

        prompt = construct_prompt(data.dict())

        travel_plan = generate_travel_plan(prompt)

        return jsonify({"travel_plan": json.loads(travel_plan)}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-location-data', methods=['POST'])
def search_places_route():
    try:
        location_name = request.json.get('location')
        if not location_name:
            return jsonify({
                "error": "Location is required"
            }), 422
        
        prompt = construct_location_prompt(location_name)
        location_data = generate_location_data(prompt)
    

        lat, lng, place_id = get_lat_lng(location_name)
        if lat is None or lng is None or place_id is None:
            return jsonify({"error": "Could not retrieve location data"}), 500
    
        search_place_details = get_place_details(place_id)
        if not search_place_details:
            return jsonify({"error": "No places details found"}), 500
        search_place_details = {
            "name": search_place_details['name'],
            "place_id": place_id,
            "rating": search_place_details.get('rating', 'N/A'),
            "user_ratings_total": search_place_details.get('user_ratings_total', 'N/A'),
            "formatted_address": search_place_details.get('formatted_address', 'N/A'),
            "opening_hours": search_place_details.get('opening_hours', {}).get('weekday_text', 'N/A'),
            "website": search_place_details.get('website', 'N/A'),
            "international_phone_number": search_place_details.get('international_phone_number', 'N/A'),
        }

        places = nearby_search(lat, lng)
        if not places:
            return jsonify({"error": "No places found nearby"}), 500
        nearby_search_places = []
        for place in places:
            place_details = get_place_details(place['place_id'])
            nearby_search_places.append({
                "name": place['name'],
                "place_id": place['place_id'],
                "business_status": place['business_status'],
                "rating": place.get('rating', 'N/A'),
                "user_ratings_total": place.get('user_ratings_total', 'N/A'),
                "types": place['types'],
                "formatted_address": place_details.get('formatted_address', 'N/A'),
                "opening_hours": place_details.get('opening_hours', {}).get('weekday_text', 'N/A'),
                "website": place_details.get('website', 'N/A'),
                "international_phone_number": place_details.get('international_phone_number', 'N/A'),
            })

        weather_data = fetch_weather_data(lat, lng, search_place_details)

        return jsonify({
            "location_data": json.loads(location_data),
            "search_place_details":search_place_details,
            "nearby_search_places": nearby_search_places,
            "weather_data": weather_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


application = app

if __name__ == "__main__":
    application.run()
