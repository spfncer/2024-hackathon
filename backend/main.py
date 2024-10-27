from typing import Union
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from json import JSONDecoder, JSONEncoder
from fastapi.encoders import jsonable_encoder
from RequestUtils import ai_structured_response

from ai import WatsonXAI
from EvacZoneCall import FloridaEmergencyFinder

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
watson = WatsonXAI()
decoder = JSONDecoder()
encoder = JSONEncoder()
finder = FloridaEmergencyFinder()

@app.get("/")
def read_root():
    logger.info(f"request / endpoint!")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    logger.info(f"request / endpoint!")
    return {"item_id": item_id, "q": q}

def get_evacuation_zone(address: str):
    logger.info(f"request / endpoint!")

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

    try:
        return finder.find_nearest_locations(address, num_results)
            
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not complete request",
        )
@app.get("/query/{query_string}")
def ai_request(query_string: str):
    logger.info(f"request / endpoint!")
    response = watson.query(query_string)
    response_array = response.split("\n")
    for (i, res) in enumerate(response_array):
        response_array[i] = res.strip().replace("- ", "")
    return response_array

def __determine_status(zone:str):
    """
    Determines the immediate action the user should prepare to take
    For demo purposes, this just switches over the evac zone
    IRL this would need to consider hurricane track and evacuation orders
    """
    if (zone == "A" or zone == "B"):
        return "evacuate"
    if (zone == "C" or zone == "D"):
        return "be_prepared"
    return "okay"

@app.get("/status/{address}")
async def get_status(address: str):
    coords = finder.geocode_address(address)
    evac_zone = get_evacuation_zone(address)
    istatus = __determine_status(evac_zone)
    response = {
        "status": istatus,
        "zone": evac_zone,
        "coords": coords
    }
    return jsonable_encoder(response)

@app.get("/results/{json_string}")
async def results(json_string: str):
    logger.info(f"request / endpoint!")
    obj = decoder.decode(json_string)
    evac_zone = get_evacuation_zone(obj.get('address'))
    ai_req = ai_structured_response(obj, evac_zone, "okay", "home", "", True)
    response = {
        "advice": ai_request(ai_req),
    }
    return jsonable_encoder(response)

@app.get("/hotels/{address}")
async def find_hotels(address:str):
    coords = finder.geocode_address(address)
    #coords = (coords[0] + 0.43, coords[1]) # go ~30 miles north, IRL would need to compute based on cone
    hotels = finder.find_nearby_hotels(coords, 5000, 3)
    response = {
        "hotels": hotels
    }
    return jsonable_encoder(response)