from flask import Flask, render_template, request, jsonify
import mapexify


app = Flask(__name__)
app.secret_key = "0123456789"
key = mapexify.get_key()


# service home page
@app.route("/")
def home() -> str:
    return render_template("home.html", key=key)

@app.route("/place", methods=["POST"])
def get_data() -> str:
    response = request.form
    country = response["country"]
    city = response["city"]
    street = response["street"]
    house = response["house"]
    postal = response["postal"]
    global data
    data = mapexify.get_data_from_api(country, city, street, house, postal)
    suggestions = mapexify.get_suggestions(data)
    return render_template("home.html", suggestions=suggestions, key=key)

@app.route("/choice", methods=["POST"])
def choice() -> str:
    response = request.form
    choice = response["suggestion"]
    json_final = mapexify.find_location_by_formatted_address(choice, data)
    return render_template("home.html", json_final=json_final, key=key)

@app.route("/path", methods=["POST"])
def path() -> str:
    response = request.get_json()
    coordinates = mapexify.get_location(response)
    api_route = mapexify.get_route_from_api(coordinates)
    route = mapexify.get_route(api_route)
    return jsonify({"route": route})

@app.route("/toll", methods=["POST"])
def toll() -> str:
    response = request.get_json()
    atributes = mapexify.get_toll_atributes(response)
    lat = atributes[0]
    lon = atributes[1]
    profile = atributes[2]
    currency = atributes[3]
    fetch = mapexify.get_toll_data_from_api(lat, lon, profile, currency)
    final = mapexify.get_result(fetch)
    converted_price = final[0]
    converted_currency = final[1]
    distance = final[2]
    time = final[3]
    return jsonify({"converted_price": converted_price, "converted_currency": converted_currency, "distance": distance, "time": time})
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)