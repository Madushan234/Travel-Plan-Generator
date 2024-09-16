def construct_prompt(data):

    budget_mapping = {
        'Low': 'a cheap budget (0-1000 USD exclusively for activities and dining)',
        'Medium': 'a moderate budget (1000-2500 USD exclusively for activities and dining)',
        'High': 'a high budget (2500+ USD exclusively for activities and dining)',
    }

    pace_mapping = {
        'Relaxed': 'Relaxed with more downtime, fewer activities per day',
        'Balanced': 'Balanced with a mix of activities and relaxation',
        'Fast-paced': 'Fast-paced with a packed itinerary and lots of activities',
    }

    cultural_pref = 'Interested in exploring the local culture and traditions' if data['culturalPreferences'] == 'Yes' else 'Prefers general tourist activities'

    experience_mapping = {
        'Beginner': 'Beginner who prefers guided tours and clear itineraries',
        'Intermediate': 'Intermediate, comfortable with some self-guided activities',
        'Expert': 'Expert, enjoys exploring off the beaten path',
    }

    accommodation_mapping = {
        'Budget': 'Budget with basic amenities',
        'Mid-range': 'Mid-range, comfortable but not extravagant',
        'Luxury': 'Luxury with high-end amenities and services',
        'No Preference': 'No specific preference for accommodation luxury level',
    }

    activities = data['activities'].replace(',', ', ')


    prompt = (
        f"Generate a travel plan for location {data['destination']} for {data['travelDays']} days for {data['travelersCount']} people with {budget_mapping.get(data['budget'], 'a specified budget')}. "
        f"Preferred travel pace is {pace_mapping.get(data['travelPace'], 'Not specified')}. "
        f"Cultural preferences: {cultural_pref}. "
        f"Travel experience: {experience_mapping.get(data['travelExperience'], 'Not specified')}. "
        f"Accommodation preference: {accommodation_mapping.get(data['accommodation'], 'Not specified')}. "
        f"Include activities and special interests like {activities}. "
        f"Provide a list of hotels with the following details: Hotel Name, Hotel Address, Geo Coordinates, Rating, and Descriptions. "
        f"Also, suggest an itinerary including: Place Name, Place Details, Geo Coordinates, Ticket Pricing, Travel Time between locations, and the best time to visit for each day. "
        f"Ensure that the response is in the following structured JSON format:\n"
        f"{{\n"
        f'    "hotels": [\n'
        f'        {{"name": "Hotel Name", "address": "Hotel Address", "geo_coordinates": {{"lat": 0.0, "lng": 0.0}}, "rating": 4.5, "description": "Hotel Description"}}\n'
        f'    ],\n'
        f'    "itinerary": [\n'
        f'        {{"day": 1, "places": [{{"name": "Place Name", "details": "Place Details", "geo_coordinates": {{"lat": 0.0, "lng": 0.0}}, "ticket_price": "10 USD", "travel_time": "30 mins", "best_time_to_visit": "Morning"}}]}}\n'
        f'    ]\n'
        f"}}"
    )
    return prompt
