# Imports
import requests
import json
import static
import os

# Metadata
__author__ = "IamKrytas"
__name__ = "Mapexify"
__version__ = "0.5.2"

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

        save_to_json_file(data)
        
        suggestions = get_suggestions(data)
        #save suggestions to file
        print(suggestions)
        return suggestions
    except:
        raise Exception("Error while getting data from API")


def get_suggestions(data) -> list:
    try:
        suggestions = []
        for i in range(len(data["locations"])):
            suggestions.append(data["locations"][i]["formattedAddress"])
        return suggestions
    except:
        raise Exception("Error while getting address")
    

def save_to_json_file(data):
    jsons = os.path.join("app", "jsons")
    if not os.path.exists(jsons):
        os.makedirs(jsons)
    try:
        data_str = json.dumps(data, ensure_ascii=False).replace("'", '"')
        with open(os.path.join(jsons, "data.json"), "w") as f:
            f.write(data_str)
    except:
        raise Exception("Error while saving to json")
    return True
    

def find_location_by_formatted_address(choice):
    with open("app/jsons/data.json", "r") as f:
        json_data = json.load(f)
    for location in json_data["locations"]:
        if location["formattedAddress"] == choice:
            return location
    return None


def get_location():
    with open ("app/jsons/path.json", "r") as f:
        data = json.load(f)
    lat = []
    lon = []
    for item in data:
        #add to lists
        lat.append(item["referencePosition"]["latitude"]) #x
        lon.append(item["referencePosition"]["longitude"]) #y
    print(lat)
    print("---------------------------------")
    print(lon)
    print("---------------------------------")
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
    print("---------------------------------")
    with open("app/jsons/route.json", "w") as f:
        f.write(json.dumps(data, ensure_ascii=False).replace("'", '"'))
        print("Saved route to file")
    return data

def get_route():
    with open("app/jsons/route.json", "r") as f:
        data = json.load(f)
        polilines = json.loads(data["polyline"])
        coordinates = polilines["coordinates"]
        print(coordinates)
    return coordinates