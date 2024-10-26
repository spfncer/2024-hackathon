from typing import Union

from fastapi import FastAPI
from ai import WatsonXAI

app = FastAPI()
watson = WatsonXAI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/query/{query_string}")
def ai_request(query_string: str):
    response = watson.query(query_string)
    response_array = response.split("\n")
    for (i, res) in enumerate(response_array):
        response_array[i] = res.strip().replace("- ", "")
    return {"response": response_array}