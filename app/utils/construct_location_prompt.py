def construct_location_prompt(data):

    prompt = (
        f"Provide detailed information about the location: {data['location']}. "
        f"Include details such as popular attractions, local culture, weather conditions, "
        f"recommended activities, and other relevant information."
    )
    return prompt