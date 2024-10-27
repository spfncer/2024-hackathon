# Evacugator

## Inspiration

As native Floridians, we have lived through numerous hurricanes throughout our lives. We have seen the tragedies that each new disaster causes firsthand. Additionally, from personal experience, we found that the people who don't evacuate tend to be people without the monetary ability or knowledge to. That is why we decided to use IBM's innovative AI technologies to try and help prevent the unnecessary loss of human life that results from these strong storms. To do this, we made an all-inclusive, easy to use app that is made to inform and assist people in evacuation zones on how to cheaply and efficiently get to safety.

## What It Does

Our Evacugator app works by first asking the user relevant questions such as where they live, how many people they live with, if they already have transportation and/or a shelter outside the storm's path, and if they have any special accommodations necessary for their survival through the storm. With the user information and real-time information about the path of the pertinent hurricane, our program will generate a user-specific evacuation plan. Plan and user information is then given to an LLM that utilizes publicly available documents on hurricane preparedness. Moreover, the AI will provide personalized guidance on how each user can prepare. Plans will include information such as the quickest route out of the hurricane's path, the possible impact of the disaster, the locations of hurricane shelters nearby, the availability of cheap hotels nearby, and, if necessary, the ability of free/cheap transportation out of the evacuation zone. Therefore, this would hopefully help the user gain the knowledge they need to safely escape the disaster.

Though we place emphasis on how end users will interact with Evacugator, the primary customer for Evacugator is governments. Evacugator seeks to provide local authorities with a direct line to reach citizens as part of orchestrating area evacuations. Though the results shown to users are highly individualistic, the goal for Evacugator is to provide citizens with a path to evcauate which aligns with coordinated evacuation efforts.

## Usage Instructions

> [!WARNING] 
> The application is not hosted, due in part to watsonx.ai access being revoked and the GoogleMaps API key being revoked once the hackathon window is over. To run, you must start the front and backends locally.

To setup & run this application, perform the following steps:
1. Set up a Google Maps API key by following the instructions here (https://developers.google.com/maps/get-started), and modifying line 14 of the `frontend/src/index.html` file to use your key instead of the provided one. 
> [!CAUTION] 
> DO NOT SHARE YOUR API KEY WITH ANYONE!
2. Set up a WatsonX API key by following the instructions from IBM and placing it in a `backend/.env` file (which you must create) in a similar format to the `sample.env` file. 
> [!CAUTION] 
> DO NOT SHARE YOUR API KEY WITH ANYONE!
3. Download frontend dependencies with the following commands: 
```
cd frontend 
npm i
```
4. Download backend dependencies with the following commands: 
```
cd backend 
pip install -r requirements.txt
```
5. Create a backend/documents directory, and populate this folder with PDF documents about hurricane preparedness. For our demo, we used documents created by the State of Florida.
> [!NOTE] 
> Depending on how your pip and python versions are installed, you may need to modify the pip install command to work for your installation. 
6. Start the backend server utilizing the following command: 
```
cd backend 
python3 -m uvicorn main:app --reload --log-config=log_conf.yaml
```
7. Start the frontend server utilizing the following command: 
```
cd frontend
npm run start
```

## How We Built It

This project utilizes the client server architecture model, and consists of a frontend and backend component (organized into folders in the GitHUB repository). Each of these components are discussed separately below.

We divided the work of developing the application into broad roles defined below:
- Gabriel Aldous - Frontend developer, integration specialist
- Benjamin Bryant - Frontend developer, web designer, external data source researcher
- Spencer Fasulo - Full-stack developer, web designer, WatsonX AI engineer
- John Spurrier - Backend developer, external data source researcher
- Jonathan Calderone - Presentation design, script design, management

### Frontend

The frontend is an Angular application which utilizes Angular v18.0.2. This framework was chosen due to developer familiarity, simplicity, and efficiency. We utilize the PrimeNG library (and related libraries all on version 18 beta) to utilize a few pre-built components and utility classes. Furthermore, we utilize the Google Maps API via the Angular Google Maps component (provided by Google, which developed Angular and Google Maps). 

There are two webpages in the frontend, the input page and the result page. The input page consists of an Angular reactive form which the users use to enter data about their situation, and this data is passed to the results page which makes queries to the backend to retrieve the data from watsonx.ai and other sources (discussed in the backend section). The results page utilizes the Google Maps API and PrimeNG components to display the fetched data in a user friendly manner. 

Both pages share a common ‘navbar’ component, which displays the application name, logo, internet connection status, and a button to open a color changing menu. The color changing menu allows users to set the primary color of the application and toggle light or dark mode. 

In addition, the frontend also has some services and utilities which are utilized globally, such as a custom utility to represent http requests as Angular signals, and a service to monitor internet connection. 

### Backend

The backend is built upon Python (versions 3.10, 3.11, and 3.12 supported) and FastAPI. There are three main files in the backend, `ai.py`, `EvacZoneCall.py`, and `main.py`.

The `ai.py` file is home to the `WatsonXAI` class, which facilitates querying watsonx.ai from Python code. 

The `EvacZoneCall.py` file is home to the `FloridaEmergencyFinder` class, which fetches information from the FEMA API, ArcGIS API, and Overpass API. This class facilitates finding evacuation zones, nearby shelters, and nearby hotels all in a single class.

FastAPI routes within `main.py` transform input from the frontend into usable formats by the `WatsonXAI` and `FloridaEmergencyFinder` classes, and then returns the results to the frontend as JSON data. 

## Challenges we ran into

### Retrieval Augmented Generation
In the watsonx.ai Prompt Lab, including documents to ground responses in was simple — but this did not translate into Python code easily. To make this key feature happen, we had to create a vector database in Python (using watsonx.ai embeddings), manually retrieve data from it, and inject that as context into the LLM. This proved a great learning exercise to better understand how LLMs can read data from contextual documents.

### Timing
The goal for Evacugator is to aid government efforts in coordinating evacuation plans by reaching citizens directly in the event of a hurricane. But there are a large number of variables that need to be considered in making those decisions which we just did not have the time to implement in this short hackathon. Still, we are proud of what we were able to accomplish — more on that below!

## Accomplishments that we're proud of

We are proud that we managed to integrate smoothly with so many external data sources (Watson, FEMA, etc). Managing all these external connections was no small feat, and the project would quickly become extremely disorganized. The fact we were able to organize all of these external services in an organized manner while under a time crunch is, in our opinion, impressive. 

Furthermore, the fact that we were able to leverage the beta version of PrimeNG to provide app customization options and a smooth user interface is something we are proud of, especially since only one developer had utilized PrimeNG in the past (and on an older version of the library too).

Additionally, all of our frontend developers learned new skills relating to Angular, including the new Angular signals, standalone components, and Angular application routing. Furthermore, the team was able to support both mobile and desktop experiences with Evacugator. 

Finally, we are proud that we managed to set up the watsonx.ai model to output a relatively detailed and relevant set of hurricane preparation steps, especially given the wide range of input parameters we are feeding to the model. Experimenting with different models and parameters, training the AI on the set of PDF files, and then having the AI generate non-gibberish output is something which took the better part of 8 hours to achieve, and was well worth it. 

## What We Learned

Our developers learned a variety of skills, including but not limited to:

1. Angular v18.0.2
    - Signals
    - Standalone Components
    - Routing

2. watsonx.ai 
    - Navigating the Prompt Lab
    - Testing different models
    - Generating API keys
    - Using watsonx.ai models with LangChain

3. External API usage
    - Google Maps API
    - Google Places API
    - FEMA API
    - ArcGIS API
    - Overpass API

## What's Next For Evacugator
### User-Facing Work
To bring Evacugator to a real-world use case, more work needs to be done. User-facing features like identifying shelters, transportation options, and evacuation status (based on realtime hurricane data) remain to be implemented. 
### Government Dashboard
Since the primary audience for Evacugator is governments, work needs to be done to develop a portal where authorities can:
- Activate/deactivate Evacugator service
- Update guidance documents leveraged by the LLM
- Control evacuation notices
- Add shelter information
- Customize the branding of Evacugator
### Beyond Hurricanes
Evacugator's next idea would be to expand the scope of this project. Right now, the app is only aimed at hurricanes in Florida. Therefore, in the future, we hope to expand it to help assist in evacuation efforts for other predictable natural disasters and for other places around the world.
