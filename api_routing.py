from contextlib import nullcontext

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/users/{id_user}/transactions")
def read_user_transactions(id_user: int):
    return nullcontext