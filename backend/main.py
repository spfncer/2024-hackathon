from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
import logging
from json import JSONDecoder, JSONEncoder
from fastapi.encoders import jsonable_encoder

from ai import WatsonXAI
from EvacZoneCall import FloridaEmergencyFinder

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
watson = WatsonXAI()
decoder = JSONDecoder()
encoder = JSONEncoder()

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
    logger.info(f"request / endpoint!")
    response = watson.query(query_string)
    response_array = response.split("\n")
    for (i, res) in enumerate(response_array):
        response_array[i] = res.strip().replace("- ", "")
    return response_array

def ai_structured_response(user_data:dict, evac_zone:int, status:str, plan:str, backup:str, state_of_emergency:bool): 
    """
    Builds a structured response for the AI to process.

    Parameters
    ----------
    user_data : dict
        The data from the form.
    evac_zone : int
        The evacuation zone of the user
    status : str
        The plan of action for the user. "home", "hotel", "family", or "shelter"
    backup : str
        The backup plan of action for the user. "hotel", "family", or "shelter"
    state_of_emergency : bool
        Whether a state of emergency has been declared.

    Returns
    -------
    str
        The structured response for the AI to process.
    """
    residencestr = ''
    statusstr = ''
    planstr = ''
    backupstr = ''
    petsstr = ''
    prescriptionstr = ''
    medicalstr = ''
    emergencystr = "A state of emergency has been declared." if state_of_emergency else "A state of emergency has not been declared."
    match user_data.get("residence_type"):
        case "House":
            residencestr = "lives in a single family home"
        case "Apartment":
            residencestr = "lives in an apartment"
        case "Mobile Home":
            residencestr = "lives in a mobile home"
        case "Dormitory":
            residencestr = "lives in a dormitory"
        case "Homeless":
            residencestr = "is homeless"
        case "Other":
            residencestr = "lives in an alternate type of residence"
    match status:
        case "okay":
            statusstr = "not under evacuation"
        case "be-prepared":
            statusstr = "under an evacuation advisory"
        case "evacuate":
            statusstr = "under a mandatory evacuation"
    match plan:
        case "home":
            planstr = "shelter in place"
        case "hotel":
            planstr = f"evacuate to a hotel via {user_data.get('travel_mode')}"
        case "family":
            planstr = f"evacuate to a family member's home via {user_data.get('travel_mode')}"
        case "shelter":
            planstr = f"evacuate to a shelter via {user_data.get('travel_mode')}"
    match backup:
        case "hotel":
            backupstr = f", but may evacuate via {user_data.get('travel_mode')} to a hotel if conditions worsen"
        case "family":
            backupstr = f", but may evacuate via {user_data.get('travel_mode')} to a family member's home if conditions worsen"
        case "shelter":
            backupstr = f", but may evacuate via {user_data.get('travel_mode')} to a shelter if conditions worsen"
        case _:
            backupstr = ""
    if (user_data.get("small_pets") or user_data.get("medium_pets") or user_data.get("large_pets")):
        petsstr = f"The user has {user_data.get('small_pets')} small pets, {user_data.get('medium_pets')} medium pets, and {user_data.get('large_pets')} large pets."
    if (user_data.get("medication") == True):
        prescriptionstr = "The user takes prescription medications."
    if (user_data.get("equipment") == True):
        medicalstr = "The user needs specialized medical equipment."
    
    query = f"The user has a household size of {user_data.get('number_people')}, and {residencestr}. They live in evacuation zone {evac_zone}, which is {statusstr}. The user will {planstr}{backupstr}. {emergencystr} {petsstr} {prescriptionstr} {medicalstr}"
    return query

@app.get("/results/{json_string}")
def results(json_string: str):
    logger.info(f"request / endpoint!")
    obj = decoder.decode(json_string)
    response = {
        "status": "okay", # "okay" or "be-prepared" or "evacuate"
        "advice": ai_request(ai_structured_response(obj, 1, "okay", "home", "", True)),
    }
    return jsonable_encoder(response)
