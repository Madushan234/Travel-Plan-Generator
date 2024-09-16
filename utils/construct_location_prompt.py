def construct_location_prompt(location):

    prompt = (
        f"Provide detailed information about the location: {location}. "
        f"Use the following structured format in JSON:\n"
        f"{{\n"
        f"    \"description\": \"Brief description of the location\",\n"
        f"    \"festivals\": \"Major festivals celebrated in the location\",\n"
        f"    \"food\": \"Popular local cuisines and food items\",\n"
        f"    \"language\": \"Common languages spoken\",\n"
        f"    \"religion\": \"Major religions followed\",\n"
        f"    \"popular_attractions\": \"List of must-visit attractions\",\n"
        f"    \"accommodation\": \"Accommodation options\",\n"
        f"    \"climate\": \"Climate details\",\n"
        f"    \"currency\": \"Local currency used\",\n"
        f"    \"safety\": \"Safety information for tourists\",\n"
        f"    \"transportation\": \"Available transportation options\",\n"
        f"    \"best_time_to_visit\": \"Recommended best time to visit\",\n"
        f"    \"recommended_activities\": \"Suggested activities for travelers\"\n"
        f"}}"
    )
    return prompt