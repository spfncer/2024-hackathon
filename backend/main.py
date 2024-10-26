from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
import logging

from ai import WatsonXAI
from EvacZoneCall import FloridaEmergencyFinder

logger = logging.getLogger(__name__)

app = FastAPI()
watson = WatsonXAI()


@app.get("/")
def read_root():
    logger.info(f"request / endpoint!")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    logger.info(f"request / endpoint!")
    return {"item_id": item_id, "q": q}

@app.get('/evacuation_zone')
async def get_evacuation_zone(address: str):
    logger.info(f"request / endpoint!")
    finder = FloridaEmergencyFinder()

    try:
        user_coords = finder.geocode_address(address)
        evacuation_zone = finder.get_evacuation_zone(user_coords)
        return evacuation_zone
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not complete request",
        )
 
@app.get('/shelters')
async def get_shelters(address: str, num_results: int):
    logger.info(f"request / endpoint!")
    finder = FloridaEmergencyFinder()

    try:
        return finder.find_nearest_locations(address, num_results)
            
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not complete request",
        )
@app.get("/query/{query_string}")
def ai_request(query_string: str):
    response = watson.query(query_string)
    response_array = response.split("\n")
    for (i, res) in enumerate(response_array):
        response_array[i] = res.strip().replace("- ", "")
    return {"response": response_array}
