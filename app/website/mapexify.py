# Imports
import requests
import json
import static
import os

# Metadata
__author__ = "IamKrytas"
__name__ = "Mapexify"
__version__ = "0.0.1"

def get_data_from_api(country: str, city: str, street: str, house: str, postal: str) -> list:
    try:
        key = static.api_key
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
        with open(os.path.join(jsons, "data.json"), "w") as f:
            f.write(str(data))
    except:
        raise Exception("Error while saving to json")
    

def find_location_by_formatted_address(choice):
    with open("app/jsons/tmp.json", "r") as f:
        json_data = json.load(f)
    for location in json_data["locations"]:
        if location["formattedAddress"] == choice:
            return location
    return None