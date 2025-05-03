from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import ast

load_dotenv()

nvidia_key = os.getenv("NVIDIA_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_key
)

trip_plan_template = {
    "trip_plan": {
        "destination": "",
        "duration_days": None,
        "duration_nights": None,
        "budget": None,
        "current_account_balance": None,
        "current_savings": None,
        "accommodation": {
            "name": "",
            "link": "",
            "total_cost": None,
            "cost_per_night": None
        },
        "transportation": {
            "suggested_airlines": [
                {
                    "name": "",
                    "link": ""
                }
            ],
            "departure_airport": "",
            "arrival_airport": "",
            "estimated_cost_range": {
                "min": None,
                "max": None
            }
        },
        "activities_and_food": {
            "daily_cost_range": {
                "min": None,
                "max": None
            },
            "suggested_activities": [""],
            "suggested_foods": [""]
        },
        "total_estimated_cost_range": {
            "min": None,
            "max": None
        },
        "budget_adjustments": [""],
        "additional_tips": [""]
    }
}


def get_agent_answer(transactions, persona_data, prompt, message_history=None, last_response=None):
    if message_history is None:
        message_history = []

    # Only add the system prompt if it's not already there
    system_prompt = (
        "You are a travel assistant that helps users plan budget-conscious vacations. "
        "You consider the user's recent transactions, financial behavior, current savings, and travel preferences. "
        "Offer realistic and financially sound suggestions for destinations, including number of days and nights, total cost estimates, and budget tips. "
        "Include specific hotel names and working links from real booking websites (like Booking.com, Expedia, Hostelworld). "
        "Include airline suggestions with real airline names and links (like Ryanair, KLM, easyJet, etc). "
        "Be concise and only reply with a JSON object matching this structure with no explanations or extra text: "
        f"{trip_plan_template} "
        "Avoid markdown, quotes, or escape characters in your response. Respond with raw JSON only."
    )

    # Construct and add new user input
    user_content = f"""
    Context:
    {message_history}
    
    Persona:
    {persona_data}

    Transactions:
    {transactions}

    Prompt:
    {prompt}
    """

    message_history.append({"role": "system", "content": system_prompt})
    message_history.append({"role": "user", "content": user_content})

    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=message_history,
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True,
    )

    try:
        response_text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content

        parsed_dict = ast.literal_eval(response_text)
        print(parsed_dict)

        return {"response": parsed_dict}

    except Exception as e:
        print("Parsing failed:", e)
        return {"response": None, "message_history": message_history}
