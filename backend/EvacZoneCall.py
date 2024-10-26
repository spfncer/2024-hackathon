import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import List, Tuple

class FloridaEmergencyFinder:
    def __init__(self):
        self.geocoder = Nominatim(user_agent="emergency_finder")
        self.fema_api_base = "https://www.fema.gov/api/open/v2"
            
    def fetch_florida_locations(self) -> List[dict]:
        """
        Fetch Florida emergency location data from FEMA's API.
        """
        try:
            endpoint = f"{self.fema_api_base}/PublicAssistanceApplicantsProgramDeliveredData"
            params = {
                "$select": "applicantId,state,countyCode,damageCategory,projectSize,projectAmount",
                "$filter": "state eq 'FL'",
                "$top": 100,
                "$orderby": "projectAmount desc"
            }
            
            response = requests.get(endpoint, params=params)
            if response.status_code != 200:
                # Fallback to Florida emergency locations if API fails
                return self.get_fallback_locations()
                
            return response.json()['PublicAssistanceApplicantsProgramDeliveredData']
                
        except Exception as e:
            print(f"API Error: {str(e)}")
            # Fallback to hardcoded data
            return self.get_fallback_locations()

    def get_fallback_locations(self) -> List[dict]:
        """
        Provide fallback emergency locations in Florida.
        """
        return [
            {
                "county": "Miami-Dade",
                "name": "Miami-Dade Emergency Operations Center",
                "address": "9300 NW 41st Street, Miami, FL 33178",
                "coordinates": (25.8180, -80.3419)
            },
            {
                "county": "Broward",
                "name": "Broward County Emergency Operations Center",
                "address": "201 NW 84th Avenue, Plantation, FL 33324",
                "coordinates": (26.1239, -80.2610)
            },
            {
                "county": "Orange",
                "name": "Orange County Emergency Operations Center",
                "address": "6590 Amory Court, Winter Park, FL 32792",
                "coordinates": (28.6077, -81.3148)
            },
            {
                "county": "Hillsborough",
                "name": "Hillsborough County EOC",
                "address": "2711 E Hanna Ave, Tampa, FL 33610",
                "coordinates": (27.9506, -82.4572)
            },
            {
                "county": "Duval",
                "name": "Duval County Emergency Operations Center",
                "address": "515 N Julia Street, Jacksonville, FL 32202",
                "coordinates": (30.3322, -81.6557)
            },
            {
                "county": "Pasco",
                "name": "Fasano Regional Shelter",
                "address": "11611 Denton Ave, Hudson, FL 34667",
                "coordinates": (28.385085, -82.642799)
            },
            {
                "county": "Hernando",
                "name": "Enrichment Centers Inc. of Hernando County",
                "address": "800 John Gary Grubbs Blvd., Brooksville, FL 34601",
                "coordinates": (28.540582, -82.389842)
            },
            {
                "county": "Polk",
                "name": "State Shelter - Auburndale (Red Cross)",
                "address": "640 C Fred Jones Blvd, Auburndale, FL 33823",
                "coordinates": (28.074387, -81.799920)
            },
            {
                "county": "Pasco",
                "name": "Wesley Chapel Recreation Complex",
                "address": "7727 Boyette Rd, Wesley Chapel, FL 33545",
                "coordinates": (28.268380, -82.327990)
            },
            {
                "county": "St. Lucie",
                "name": "First United Methodist of Port St. Lucie (Red Cross)",
                "address": "260 SW Prima Vista Blvd, Port St. Lucie, FL 34983",
                "coordinates": (27.314657, -80.362488)
            },
            {
                "county": "Manatee",
                "name": "First United Methodist Church (Red Cross)",
                "address": "603 11th St W, Bradenton, FL 34205",
                "coordinates": (27.492999, -82.568684)
            },
            {
                "county": "Pinellas",
                "name": "State Shelter - Light of Christ Shelter (Red Cross)",
                "address": "2176 Marilyn St, Clearwater, FL 33765",
                "coordinates": (27.977335, -82.742178)
            },
            {
                "county": "Hillsborough",
                "name": "State Shelter - Tampa All Peoples (Red Cross)",
                "address": "6105 E Sligh Ave, Tampa, FL 33617",
                "coordinates": (28.013182, -82.386221)
            },
            {
                "county": "Charlotte",
                "name": "State Shelter - Harold Avenue Park Recreation Center (Red Cross)",
                "address": "23400 Harold Ave, Port Charlotte, FL 33980",
                "coordinates": (26.990759, -82.058659)
            }
        ]

    def format_address(self, address: str) -> str:
        """
        Format the address to ensure it includes Florida if not specified.
        """
        lower_address = address.lower()
        if 'fl' not in lower_address and 'florida' not in lower_address:
            address += ', Florida'
        return address

    def geocode_address(self, address: str) -> Tuple[float, float]:
        """
        Convert an address to latitude and longitude coordinates.
        """
        try:
            formatted_address = self.format_address(address)
            location = self.geocoder.geocode(formatted_address)
            if location:
                return (location.latitude, location.longitude)
            else:
                raise ValueError("Address not found. Please provide more details.")
        except Exception as e:
            raise Exception(f"Error geocoding address: {str(e)}")

    def get_evacuation_zone(self, coordinates: Tuple[float, float]) -> str:
        """
        Get the evacuation zone for the given coordinates.
        """
        try:
            endpoint = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Evacuation_Zones/FeatureServer/0/query"
            
            params = {
                "f": "json",
                "geometry": f"{coordinates[1]},{coordinates[0]}",  # longitude,latitude
                "geometryType": "esriGeometryPoint",
                "inSR": "4326",
                "spatialRel": "esriSpatialRelIntersects",
                "outFields": "*",
                "returnGeometry": "false"
            }
            
            response = requests.get(endpoint, params=params)
            if response.status_code != 200:
                raise Exception(f"Error querying evacuation zone: HTTP {response.status_code}")
            
            data = response.json()
            
            if data and "features" in data and data["features"]:
                attributes = data["features"][0]["attributes"]
                evacuation_zone = attributes.get("EZone", "Unknown")
                return evacuation_zone
            else:
                return "Not in an evacuation zone"
        except Exception as e:
            raise Exception(f"Error retrieving evacuation zone: {str(e)}")

    def find_nearest_locations(self, address: str, num_results: int = 3) -> List[dict]:
        """
        Find the nearest emergency locations to the given address in Florida.
        """
        try:
            # Get coordinates for the input address
            user_coords = self.geocode_address(address)
            
            # Get Florida location data
            locations = self.fetch_florida_locations()
            
            # Calculate distances to all locations
            locations_with_distances = []
            for location in locations:
                distance = geodesic(user_coords, location['coordinates']).miles
                locations_with_distances.append({
                    "name": location['name'],
                    "county": location['county'],
                    "address": location['address'],
                    "distance": round(distance, 2)
                })
            
            # Sort by distance and return the nearest locations
            return sorted(locations_with_distances, key=lambda x: x['distance'])[:num_results]
                
        except Exception as e:
            raise Exception(f"Error finding nearest locations: {str(e)}")

    def print_location_results(self, locations: List[dict]):
        """
        Print the emergency location results in a formatted way.
        """
        print("\nNearest Emergency Operations Centers in Florida:")
        print("-" * 70)
        for i, location in enumerate(locations, 1):
            print(f"{i}. {location['name']}")
            print(f"   County: {location['county']}")
            print(f"   Address: {location['address']}")
            print(f"   Distance: {location['distance']} miles")
            print("-" * 70)

def main():
    finder = FloridaEmergencyFinder()
    
    print("Address Input Guide:")
    print("- Minimum required: Street number, street name, and city")
    print("- Example 1: '123 Main Street, Miami'")
    print("- Example 2: '456 Ocean Drive, Orlando, FL'")
    print("- Example 3: '789 Palm Avenue, Tampa, Florida'")
    print("\nNote: If you don't include 'FL' or 'Florida', it will be added automatically")
    
    try:
        address = input("\nEnter your address: ")
        user_coords = finder.geocode_address(address)
        evacuation_zone = finder.get_evacuation_zone(user_coords)
        print(f"\nEvacuation Zone for your address: {evacuation_zone}")
        nearest_locations = finder.find_nearest_locations(address)
        finder.print_location_results(nearest_locations)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
