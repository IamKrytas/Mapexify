from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import mapexify

app = Flask(__name__)
app.secret_key = "0123456789"

# service home page
@app.route("/")
def home():
    return render_template("home.html")

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
    return render_template("home.html", suggestions=suggestions)

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
    return render_template("home.html", json_final=json_final)

@app.route("/path", methods=["POST"])
def path():
    try:
        data = request.get_json()
        print("-------------------------------")
        print(data)
        print("-------------------------------")
        mapexify.get_location(data)

        # Tutaj możesz przetwarzać dane i wykonywać odpowiednie operacje

        return jsonify({"message": "Dane odebrane poprawnie."})  # Odpowiedź zwrotna w formacie JSON

    except Exception as e:
        print("Błąd podczas przetwarzania danych:", e)
        return jsonify({"error": "Błąd podczas przetwarzania danych."}), 500  # Odpowiedź błędu w formacie JSON


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)