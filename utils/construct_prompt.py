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
        f"Provide a list of hotels with the following details: Hotel Name, Hotel Address, Price, Hotel Image URL, Geo Coordinates, Rating, and Descriptions. "
        f"Also, suggest an itinerary including: Place Name, Place Details, Place Image URL, Geo Coordinates, Ticket Pricing, Travel Time between locations for {data['travelDays']} days, with each day's plan including the best time to visit. "
        f"Additionally, include the weather condition for each place in JSON format."
    )
    
    return prompt
