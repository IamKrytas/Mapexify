from flask import Flask, render_template, request, flash, jsonify
import static
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
    request_data = request.form
    print(request_data)
    country = request_data["country"]
    city = request_data["city"]
    street = request_data["street"]
    house = request_data["house"]
    postal = request_data["postal"]
    suggestions = mapexify.get_data_from_api(country, city, street, house, postal)
    return render_template("home.html", suggestions=suggestions, key=key)

@app.route("/choice", methods=["POST"])
def choice():
    request_data = request.form
    print(request_data)
    choice = request_data["suggestion"]
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
    route = mapexify.get_route()
    return jsonify(route)
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)