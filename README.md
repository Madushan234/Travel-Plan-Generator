# Travel Plan Generator API

This project provides a REST API for generating travel plans. The API accepts user inputs such as destination, travel days, number of travelers, budget, travel pace, cultural preferences, and more to generate a detailed travel plan, including hotel options, itineraries, and weather conditions.


## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Project Structure
- `app/`: Contains the main application logic.
- `config/`: Contains configuration files.
- `requirements.txt`: Lists project dependencies.


## Features
- Generates a detailed travel plan including hotel options, itineraries, and weather conditions.
- Accepts various inputs like destination, travel duration, budget, travel pace, cultural preferences, etc.
- Create personalized travel itineraries.


## Installation
1. Install the dependencies:
2. Set the `GOOGLE_API_KEY` environment variable.
3. Run the application: `python app/main.py`


## Usage
- **Endpoint**: `/generate-travel-plan`
- **Method**: POST
- **Request Body**:
```json
{
 "destination": "Galle",
 "travelDays": 3,
 "travelersCount": 2,
 "budget": "Low",
 "travelPace": "Relaxed",
 "culturalPreferences": "Yes",
 "foodPreferences": "Vegetarian",
 "travelExperience": "Intermediate",
 "accommodation": "Mid-range",
 "activities": ["Beaches", "City Sightseeing", "Food Exploration"]
}

curl -X POST http://localhost:5000/get-location-data \
-H "Content-Type: application/json" \
-d '{
  "location": "Paris"
}'
