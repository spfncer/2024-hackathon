# EvacUGator

## Inspiration

As native Floridians, we have lived through numerous hurricanes throughout our lives. We have seen the tragedies that each new disaster causes firsthand. Additionally, from personal experience, we found that the people who don't evacuate tend to be people without the monetary ability or knowledge to. That is why we decided to use IBM's innovative AI technologies to try and help prevent the unnecessary loss of human life that inevitably results from these strong storms. To do this, we made an all-inclusive, easy to use app that is made to inform and assist people in evacuation zones on how to cheaply and efficiently get to safety.

## What It Does

Our EvacUGator app works by first asking the user relevant questions such as where they live, how many people they live with, if they already have transportation and/or a shelter outside the storm's path, and if they have any special accommodations necessary for their survival through the storm. It then takes this information and feeds it to an specialized AI bot that has been trained using a lot of publicly available hurricane satellite data. With the user information and real-time information about the path of the pertinent hurricane, this AI will proceed to generate user-specific evacuation plans. These plans will include information such as the quickest route out of the hurricane's path, the possible impact of the disaster, the locations of hurricane shelters nearby, the availability of cheap hotels nearby, and, if necessary, the ability of free/cheap transportation out of the evacuation zone. Therefore, this would hopefully help the user gain the knowledge they need to safely escape the disaster.

## Usage Instructions

> [!WARNING] 
> The application is not hosted in a website, due in part to WatsonAI access being revoked and the GoogleMaps API key being revoked once the hackathon window is over. To run, you must start the front and backends locally.

To setup & run this application, perform the following steps:
1. Set up a Google Maps API key by following the instructions here (https://developers.google.com/maps/get-started), and modifying line 14 of the `frontend/src/index.html` file to use your key instead of the provided one. 
> [!CRITICAL] 
> DO NOT SHARE YOUR API KEY WITH ANYONE!
2. Set up a WatsonX API key by following the instructions from IBM and placing it in a `backend/.env` file (which you must create) in a similar format to the `sample.env` file. 
> [!CRITICAL] 
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
> [!NOTE] 
> Depending on how your pip and python versions are installed, you may need to modify the pip install command to work for your installation. 
5. Start the backend server utilizing the following command: 
```
cd backend 
python3 -m uvicorn main:app --reload --log-config=log_conf.yaml
```
6. Start the frontend server utilizing the following command: 
```
cd frontend
npm run start
```

## How We Built It

This project utilizes the client server architecture model, and consists of a frontend and backend component (organized into folders in the GitHUB repository). Each of these components are discussed separately below.

We divided the work of developing the application into broad roles defined below:
- Gabriel Aldous - Frontend developer, integration specialist
- Benjamin Bryant - Frontend developer, web designer, external data source researcher
- Spencer Fasulo - Backend developer, web designer, WatsonX AI engineer
- John Spurrier - Backend developer, external data source researcher
- Jonathan Calderone - Presentation design, script design, management

### Frontend

The frontend is an Angular application which utilizes Angular v18.0.2. This framework was chosen due to developer familiarity, simplicity, and efficiency. We utilize the PrimeNG library (and related libraries all on version 18 beta) to utilize a few pre-built components and utility classes. Furthermore, we utilize the Google Maps API via the Angular Google Maps component (provided by Google, which developed Angular and Google Maps). 

There are two webpages in the frontend, the input page and the result page. The input page consists of an Angular reactive form which the users use to enter data about their situation, and this data is passed to the results page which makes queries to the backend to retrieve the data from Watson and other sources (discussed in the backend section). The results page utilizes the Google Maps API and PrimeNG components to display the fetched data in a user friendly manner. 

Both pages share a common ‘navbar’ component, which displays the application name, logo, internet connection status, and a button to open a color changing menu. The color changing menu allows users to set the primary color of the application and toggle light or dark mode. 

In addition, the frontend also has some services and utilities which are utilized globally, such as a custom utility to represent http requests as Angular signals, and a service to monitor internet connection. 

### Backend

The backend is built upon Python (versions 3.10, 3.11, and 3.12 supported) and FastAPI. There are three main files in the backend, `ai.py`, `EvacZoneCall.py`, and `main.py`.

The `ai.py` file is home to the `WatsonXAI` class, which facilitates querying WatsonX from arbitrary Python code. 

The `EvacZoneCall.py` file is home to the `FloridaEmergencyFinder` class, which fetches information from the FEMA API, arcgis API, and overpass API. This class facilitates finding evacuation zones, nearby shelters, and nearby hotels all in a single class.

FastAPI routes within `main.py` transform input from the frontend into usable formats by the `WatsonXAI` and `FloridaEmergencyFinder` classes, and then returns the results to the frontend as JSON data. 

## Challenges we ran into

Some challenges we ran into include tuning WatsonAI to (), and modifying WatsonAI to (). 

## Accomplishments that we're proud of

We are proud that we managed to integrate smoothly with so many external data sources (Watson, FEMA, etc). Managing all these external connections was no small feat, and the project would quickly become extremely disorganized. The fact we were able to organize all of these external services in an organized manner while under a time crunch is, in our opinion, impressive. 


Furthermore, the fact that we were able to leverage the beta version of PrimeNG to provide app customization options and a smooth user interface is something we are proud of, especially since only one developer had utilized PrimeNG in the past (and on an older version of the library too).

Additionally, all of our frontend developers learned new skills relating to Angular, including the new Angular signals, standalone components, and angular application routing. 

Finally, we are proud that we managed to set up the Watson AI model to output a relatively detailed and relevant set of hurricane preparation steps, especially given the wide range of input parameters we are feeding to the model. Training the AI on the set of PDF files and then having the AI generate non-gibberish output is something which took the better part of 8 hours to achieve, and was well worth it. 

## What We Learned

Our developers learned a variety of skills, including but not limited to:

1. Angular v18.0.2
    - Signals
    - Standalone Components
    - Routing

2. WatsonAI 
    - .

3. External API usage
    - Google Maps API
    - FEMA API
    - ArcGIS API
    - Overpass API

## What's Next For EvacUGator

EvacUGator's next idea would be to expand the scope of this project. Right now, the app is only aimed at hurricanes in Florida. Therefore, in the future, we hope to expand it to help assist in evacuation efforts for other natural disasters and for other places around the world.
