from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os
import requests
import json
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# LOAD MODEL FILES
# =========================
model = pickle.load(open(os.path.join(BASE_DIR, "crop_model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "scaler.pkl"), "rb"))
label_encoder = pickle.load(open(os.path.join(BASE_DIR, "label_encoder.pkl"), "rb"))

# =========================
# PLANT DISEASE MODEL
# =========================
disease_model = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "models", "trained_plant_disease_model.keras")
)


# =========================
# WEATHER API
# =========================
WEATHER_API_KEY = os.getenv(
    "WEATHER_API_KEY",
    "d7e29ab33ef8cd0ad460f145b3a3e74f"
)

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/crop")
def crop_page():
    return render_template("crop.html")


@app.route("/calendar")
def calendar_page():
    return render_template("calendar.html")


@app.route("/market")
def market_page():
    return render_template("market.html")


@app.route("/weather_page")
def weather_page():
    return render_template("weather.html")


@app.route("/nutrition")
def nutrition_page():
    return render_template("nutrition.html")


@app.route("/disease")
def disease_page():
    return render_template("disease.html")


# =========================
# WEATHER (CITY)
# =========================
@app.route("/weather")
def weather():

    city = request.args.get("city", "Delhi")

    try:

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        res = requests.get(url, params=params)

        data = res.json()

        if res.status_code != 200:

            return jsonify({
                "error": "Invalid city"
            })

        return jsonify({

            "city": data.get("name"),

            "temp": data["main"]["temp"],

            "humidity": data["main"]["humidity"],

            "condition": data["weather"][0]["main"]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================
# WEATHER BY COORDS
# =========================
@app.route("/weather_by_coords")
def weather_by_coords():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        res = requests.get(url, params=params)

        data = res.json()

        return jsonify({

            "city": data.get("name"),

            "temp": data["main"]["temp"],

            "humidity": data["main"]["humidity"],

            "condition": data["weather"][0]["main"]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================
# MARKET TREND DATASET
# =========================
@app.route("/market_data")
def market_data():

    crop = request.args.get("crop")

    if not crop:

        return jsonify({
            "error": "Crop is required"
        })

    try:

        file_path = os.path.join(
            BASE_DIR,
            "data",
            "commodity_price.csv"
        )

        df = pd.read_csv(file_path)

        # FILTER CROP
        filtered = df[
            df["Commodity"].str.lower() == crop.lower()
        ]

        if filtered.empty:

            return jsonify({
                "error": "No market data found"
            })

        # TOP MARKETS
        top_markets = filtered.sort_values(
            by="Modal_x0020_Price",
            ascending=False
        ).head(10)

        table_data = []

        for _, row in top_markets.iterrows():

            table_data.append({

                "market": row["Market"],

                "state": row["State"],

                "commodity": row["Commodity"],

                "modal_price": int(row["Modal_x0020_Price"])
            })

        # BEST MARKET
        best = top_markets.iloc[0]

        best_market = {

            "market": best["Market"],

            "state": best["State"],

            "modal_price": int(best["Modal_x0020_Price"])
        }

        # TREND DATA
        trend = []

        trend_data = filtered.tail(10)

        for _, row in trend_data.iterrows():

            trend.append({

                "arrival_date": row["Arrival_Date"],

                "modal_price": int(row["Modal_x0020_Price"])
            })

        return jsonify({

            "best_market": best_market,

            "top": table_data,

            "trend": trend
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================
# CROP NUTRITION
# =========================
@app.route("/crop_nutrition")
def crop_nutrition():

    crop = request.args.get("crop")

    try:

        with open(os.path.join(BASE_DIR, "data", "nutrition.json")) as f:

            data = json.load(f)

        crop = crop.strip().capitalize()

        if crop not in data:

            return jsonify({
                "error": "Crop not found"
            })

        return jsonify(data[crop])

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================
# CROP PREDICTION
# =========================
@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        features = [

            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(data["temperature"]),
            float(data["humidity"]),
            float(data["ph"]),
            float(data["rainfall"])
        ]

        scaled = scaler.transform([features])

        pred = model.predict(scaled)

        crop = label_encoder.inverse_transform(pred)[0]

        return jsonify({

            "success": True,

            "crop": crop
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)
        })



# =========================
# PLANT DISEASE DETECTION
# =========================
@app.route("/predict_disease", methods=["POST"])
def disease_prediction():

    try:

        if "image" not in request.files:
            return jsonify({
                "error": "No image uploaded"
            })

        file = request.files["image"]

        if file.filename == "":
            return jsonify({
                "error": "No image selected"
            })

        # =========================
        # CREATE UPLOAD FOLDER
        # =========================
        upload_folder = os.path.join(
            BASE_DIR,
            "static",
            "uploads"
        )

        os.makedirs(upload_folder, exist_ok=True)

        # =========================
        # SAVE IMAGE
        # =========================
        filename = secure_filename(file.filename)

        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        # =========================
        # LOAD IMAGE
        # =========================
        img = image.load_img(
            filepath,
            target_size=(128, 128)
        )

        img_array = image.img_to_array(img)

        img_array = np.expand_dims(img_array, axis=0)

        img_array = img_array / 255.0

        # =========================
        # PREDICTION
        # =========================
        prediction = disease_model.predict(img_array)

        predicted_index = np.argmax(prediction)

        confidence = float(np.max(prediction)) * 100

        # =========================
        # LOAD CLASS NAMES
        # =========================
        class_file = os.path.join(
            BASE_DIR,
            "models",
            "class_indices.json"
        )

        with open(class_file, "r") as f:
            class_indices = json.load(f)

        # REVERSE DICTIONARY
        class_names = {
            v: k for k, v in class_indices.items()
        }

        disease_name = class_names[predicted_index]

        # =========================
        # DISEASE SOLUTIONS
        # =========================
        solutions = {

            "Tomato___Early_blight":
                "Use fungicide regularly and avoid overhead watering.",

            "Tomato___Late_blight":
                "Remove infected leaves immediately and use copper fungicide.",

            "Potato___Early_blight":
                "Improve air circulation and apply fungicide.",

            "Potato___Late_blight":
                "Destroy infected plants and avoid excess moisture.",

            "Corn___Common_rust":
                "Use resistant crop varieties and fungicides.",

            "Healthy":
                "Plant is healthy. Maintain proper irrigation and nutrition."
        }

        solution = solutions.get(
            disease_name,
            "Consult agricultural expert for treatment."
        )

        # =========================
        # RETURN RESULT
        # =========================
        return jsonify({

            "disease": disease_name,


            "solution": solution,

            "image": f"/static/uploads/{filename}"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)