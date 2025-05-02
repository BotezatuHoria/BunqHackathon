from contextlib import nullcontext

from fastapi import FastAPI
from util_transactions import get_all_transactions
from ai_agent import  get_agent_answer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/users/{id_user}/transactions")
async def read_user_transactions(id_user: int):
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

    get_agent_answer(result)

    return {"transactions": result}
