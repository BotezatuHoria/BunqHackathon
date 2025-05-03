from contextlib import nullcontext

from fastapi import FastAPI
from fastapi import Request

from util_transactions import get_all_transactions, get_user_balance_from_user_api
from ai_agent import  get_agent_answer

app = FastAPI()

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
        return {"transactions" : {}}

    result = []
    for payment in payments :
        result.append({
            "id": payment.id_,
            "amount": {
                "value": payment.amount.value,
                "currency": payment.amount.currency
            },
            "description": payment.description,
            "created": payment.created.isoformat() if hasattr(payment.created, "isoformat") else str(payment.created)
        })

    person_data = get_user_balance_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0")

    ans = get_agent_answer(result, person_data, prompt_bdy)

    return {"promp-asnwer": ans}
