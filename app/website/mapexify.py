# Imports
import requests
import json
import static


# Metadata
__author__ = "IamKrytas"
__name__ = "Mapexify"
__version__ = "0.6.1"


def get_key() -> str:
    return static.api_key_2

def get_data_from_api(country: str, city: str, street: str, house: str, postal: str) -> list:
    try:
        key = get_key()
        url = f"https://api.myptv.com/geocoding/v1/locations/by-address?country={country}&locality={city}&postalCode={postal}&street={street}&houseNumber={house}"
        headers = {
            "apiKey": key
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    except:
        raise Exception("Error while getting data from api")

def get_suggestions(data) -> list:
    suggestions = []
    for i in range(len(data["locations"])):
        suggestions.append(data["locations"][i]["formattedAddress"])
    return suggestions    

def find_location_by_formatted_address(choice, data):
    for location in data["locations"]:
        if location["formattedAddress"] == choice:
            return location
    return None

def get_location(response):
    locations = json.loads(response)
    lon = []
    lat = []
    for item in locations:
        lat.append(item["referencePosition"]["latitude"])
        lon.append(item["referencePosition"]["longitude"])
    return lat, lon

def get_route_from_api(cordinates):
    lat = cordinates[0]
    lon = cordinates[1]
    key = get_key()

    for i in range(len(lat)):
        if i == 0:
            url = f"https://api.myptv.com/routing/v1/routes?waypoints={lat[i]},{lon[i]}"
        else:
            url += f"&waypoints={lat[i]},{lon[i]}"

    url += "&results=POLYLINE&options[trafficMode]=AVERAGE"        
    headers = {
        "apiKey": key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_route(api_route):
    polilines = json.loads(api_route["polyline"])
    coordinates = polilines["coordinates"]
    return coordinates

def get_toll_atributes(response):
    locations = json.loads(response['localStorageData'])
    latitude = []
    longitude = []

    if "profile" in response:
        profile = response['profile']

    if "currency" in response:
        currency = response['currency']

    for location in locations:
        if 'referencePosition' in location:
            latitude.append(location['referencePosition']['latitude'])
            longitude.append(location['referencePosition']['longitude'])
            
    return latitude, longitude, profile, currency

def get_toll_data_from_api(lat: list, lon: list, profile: str, currency: str):
    key = get_key()
    for i in range(len(lat)):
        if i == 0:
            url = f"https://api.myptv.com/routing/v1/routes?waypoints={lat[i]},{lon[i]}"
        else:
            url += f"&waypoints={lat[i]},{lon[i]}"
    url += f"&profile={profile}&results=TOLL_COSTS&options[currency]={currency}&options[trafficMode]=AVERAGE"
    headers = {
        "apiKey": key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_price(data):
    price = data["toll"]["costs"]["convertedPrice"]["price"]
    currency = data["toll"]["costs"]["convertedPrice"]["currency"]
    distance = data["distance"]
    travel_time = data["travelTime"]
    distance = round(distance / 1000, 3)
    hours = travel_time // 3600
    minutes = (travel_time % 3600) // 60
    travel_time = f"{hours}h {minutes}m"
    return price, currency, distance, travel_time