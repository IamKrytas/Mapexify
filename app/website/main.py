from flask import Flask, render_template, request, flash, jsonify
import mapexify
import json

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
    return render_template("home.html", json_final=json_final, key=key)

@app.route("/path", methods=["POST"])
def path():
    data = request.get_json()
    with open ("app/jsons/path.json", "w") as f:
        f.write(data)
    coordinates = mapexify.get_location()
    mapexify.get_route_from_api(coordinates)
    route = mapexify.get_route()
    return jsonify({"route": route})

@app.route("/toll", methods=["POST"])
def toll():
    data = request.get_json()
    lat = mapexify.get_toll_atributes(data)[0]
    lon = mapexify.get_toll_atributes(data)[1]
    profile = mapexify.get_toll_atributes(data)[2]
    currency = mapexify.get_toll_atributes(data)[3]
    fetch = mapexify.get_toll_data_from_api(lat, lon, profile, currency)
    converted_price = mapexify.get_price(fetch)[0]
    converted_currency = mapexify.get_price(fetch)[1]
    distance = mapexify.get_price(fetch)[2]
    time = mapexify.get_price(fetch)[3]
    return jsonify({"converted_price": converted_price, "converted_currency": converted_currency, "distance": distance, "time": time})
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)