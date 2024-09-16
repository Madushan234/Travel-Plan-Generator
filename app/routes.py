from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from .models.travel_plan_request import TravelPlanRequest
from .models.location_request import LocationRequest 
from .services import generate_location_data, generate_travel_plan
from .utils.construct_prompt import construct_prompt
from .utils.construct_location_prompt import construct_location_prompt 

# Define a Blueprint for travel plan routes
travel_plan_bp = Blueprint('travel_plan', __name__)


@travel_plan_bp.route('/generate-travel-plan', methods=['POST'])
def generate_travel_plan_route():
    try:
        # Parse and validate the request data using the Pydantic model
        data = TravelPlanRequest(**request.json)

        # Construct the prompt using the validated data
        prompt = construct_prompt(data.dict())

        # Generate the travel plan using the AI service
        travel_plan = generate_travel_plan(prompt)

        return jsonify({"travel_plan": travel_plan}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@travel_plan_bp.route('/get-location-data', methods=['POST'])
def get_location_data_route():
    try:
        # Parse and validate the request data using the new Pydantic model
        data = LocationRequest(**request.json)

        # Construct the prompt using the validated data
        prompt = construct_location_prompt(data.dict())

        # Generate location data using the AI service
        location_data = generate_location_data(prompt)

        return jsonify({"location_data": location_data}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    except Exception as e:
        return jsonify({"error": str(e)}), 500