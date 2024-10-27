def ai_structured_response(user_data:dict, evac_zone:str, status:str, plan:str, backup:str, state_of_emergency:bool): 
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