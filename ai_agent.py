from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import  ast

load_dotenv()

nvidia_key = os.getenv("NVIDIA_KEY")

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = nvidia_key
)

trip_plan_template = {
    "trip_plan": {
        "destination": "",
        "duration_days": None,
        "duration_nights": None,
        "budget": None,
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


def get_agent_answer(transactions, persona_data, prompt) :
  system_prompt = (
    "You are a travel assistant that helps users plan budget-conscious vacations. "
    "You consider the user's recent transactions, financial behavior, current savings, and travel preferences. "
    "Offer realistic suggestions for destinations, links to hotels, costs, number of days, and transportation (plane tickets with links). "
    "Tailor it to the user profile and finances."
    f"When sending the answer do not include any markdown formatting, quotes, or escape characters. Respond with raw JSON only.:{trip_plan_template}"
  )

  user_content = f"""
      Persona:
      {persona_data}

      Transactions:
      {transactions}

      Prompt:
      {prompt}
      """

  completion = client.chat.completions.create(
    model="meta/llama-3.3-70b-instruct",
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_content}
    ],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=True,
  )

  try :
      response_text = ""
      for chunk in completion:
        if chunk.choices[0].delta.content is not None:
          response_text += chunk.choices[0].delta.content

      parsed_dict = ast.literal_eval(response_text)

      # Now it's a proper Python dict
      print(parsed_dict)

      return {"response": parsed_dict}
  except :
      return {"response" : None}