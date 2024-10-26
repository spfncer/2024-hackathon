from typing import Union

from fastapi import FastAPI, HTTPException
from starlette import status
import logging

from EvacZoneCall import FloridaEmergencyFinder

logger = logging.getLogger(__name__)
app = FastAPI()


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