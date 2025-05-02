from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

nvidia_key = os.getenv("NVIDIA_KEY")

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = nvidia_key
)

def get_agent_answer(transactions, persona_data, prompt) :
  system_prompt = (
    "You are a travel assistant that helps users plan budget-conscious vacations. "
    "You consider the user's recent transactions, financial behavior, current savings, and travel preferences. "
    "Offer realistic suggestions for destinations, links to hotels, costs, number of days, and transportation (plane tickets with links). "
    "Tailor it to the user profile and finances."
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
    stream=True
  )

  for chunk in completion:
    if chunk.choices[0].delta.content is not None:
      print(chunk.choices[0].delta.content, end="")