import json
from contextlib import nullcontext

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from util_transactions import get_all_transactions, get_user_balance_from_user_api, get_user_details
from ai_agent import get_agent_answer, last_response, has_last_response

app = FastAPI()
user_chat_state = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],  # or explicitly: ["POST", "OPTIONS"]
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/users/{id_user}/transactions")
async def read_user_transactions(id_user: int, request: Request):
    body = await request.json()
    prompt_bdy = body.get("prompt")

    payments = get_all_transactions(id_user)
    if not payments:
        print("No transactions foundsssss.")

    result = []
    if len(payments)>0:
        for payment in payments:
            result.append({
                "id": payment.id_,
                "amount": {
                    "value": payment.amount.value,
                    "currency": payment.amount.currency
                },
                "description": payment.description,
                "created": payment.created.isoformat() if hasattr(payment.created, "isoformat") else str(payment.created)
            })

    person_data = get_user_details(id_user)

    # 🔍 Detect modification intent
    prev_response = has_last_response()
    ans=""
    if prev_response is None:
        ans = get_agent_answer(result, person_data, prompt_bdy)
    else:
        prompt_bdy2=("Now, I will give you a json and a task. If I want you to modify this json, than modify it but do not change the destination from the json if I did not tell you!"
                  #   " If what I tell you sounds like modifying the details in the json that I gave you such as the duration_days, then modify them, but keep it relevant."
                     f"The json is: {json.dumps(prev_response )}\n And the task is: {prompt_bdy}")
        ans = get_agent_answer(result, person_data, prompt_bdy2)

    return {"prompt-answer": ans}
