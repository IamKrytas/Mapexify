from flask import Flask, render_template, request, flash, jsonify
import mapexify

app = Flask(__name__)
app.secret_key = "0123456789"
key = mapexify.get_key()

# service home page
@app.route("/")
def home():
    return render_template("home.html", key=key)

@app.route("/", methods=["POST"])
def get_data():
    response = request.form
    print(response)
    country = response["country"]
    city = response["city"]
    street = response["street"]
    house = response["house"]
    postal = response["postal"]
    suggestions = mapexify.get_data_from_api(country, city, street, house, postal)
    return render_template("home.html", suggestions=suggestions, key=key)

@app.route("/choice", methods=["POST"])
def choice():
    response = request.form
    print(response)
    choice = response["suggestion"]
    print(choice)
    json_final = mapexify.find_location_by_formatted_address(choice)
    print(json_final)
    flash("Added your location", "success")
    #send json_final to frontend
    return render_template("home.html", json_final=json_final, key=key)

@app.route("/path", methods=["POST"])
def path():
    data = request.get_json()
    with open ("app/jsons/path.json", "w") as f:
        f.write(data)
    coordinates = mapexify.get_location()
    mapexify.get_route_from_api(coordinates)
    route = mapexify.get_route()[0]
    distance = mapexify.get_route()[1]
    travel_time = mapexify.get_route()[2]
    return jsonify({"route": route, "distance": distance, "travel_time": travel_time})

@app.route("/toll", methods=["POST"])
def toll():
    response = request.get_json()
    print(response)
    #TODO: get toll from api
    return jsonify({"toll": "toll"})
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)