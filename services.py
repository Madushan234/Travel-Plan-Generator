import google.generativeai as genai
from config.config import get_api_key

def configure_genai():

    genai.configure(api_key=get_api_key())

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    )

def generate(prompt):

    model = configure_genai()
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            }
        ]
    )
    response = chat_session.send_message(prompt)
    return response.text


def generate_travel_plan(prompt):

    data = generate(prompt)
    return data


def generate_location_data(prompt):

    data = generate(prompt)
    return data