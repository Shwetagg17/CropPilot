# 🌾 CropPilot — AI-Powered Smart Farming Assistant

**CropPilot** is a Flask-based smart farming application that combines **machine learning, computer vision, weather data, market intelligence, crop nutrition, and farm planning** in one platform.

The goal is to help users turn soil, climate, plant-image, weather, and market data into practical agricultural insights.

---

## 🚀 Features

### 🌱 1. Smart Crop Recommendation
Predict a suitable crop from seven soil and environmental inputs:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

The application preprocesses the inputs, applies the trained ML model, and returns the predicted crop.

### 🍃 2. Plant Disease Detection
Upload a plant-leaf image and the CNN-based disease model:

- Processes the image at 128 × 128 resolution
- Predicts the supported disease class
- Returns a confidence score
- Provides a basic treatment/management suggestion
- Displays the uploaded image

### 🌦️ 3. Weather Intelligence
Weather information can be retrieved using:

- City name
- Latitude and longitude

The application returns information such as temperature, humidity, and weather condition using the OpenWeather API.

### 📊 4. Agricultural Market Trends
Select a crop to view available market information from the project's commodity-price dataset.

The market module provides:

- Top markets by modal price
- State and market information
- Crop-specific price data
- Recent price-trend data
- Highest-price market from the available dataset

### 📅 5. Crop Calendar
A dedicated calendar interface helps organize crop-related activities and farming timelines.

### 🥗 6. Crop Nutrition
The nutrition module provides crop-specific information from the project's nutrition dataset.

---

## 🧠 Machine Learning

Crop recommendation uses a trained classification workflow:

```text
User Inputs
   ↓
Data Validation
   ↓
Feature Scaling
   ↓
ML Classification Model
   ↓
Label Decoding
   ↓
Crop Recommendation
```

The disease-detection workflow uses a TensorFlow/Keras image-classification model:

```text
Leaf Image
   ↓
Resize to 128 × 128
   ↓
Normalize Pixel Values
   ↓
CNN Model
   ↓
Predicted Class + Confidence
   ↓
Treatment Suggestion
```

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Backend | Python, Flask |
| Machine Learning | Scikit-learn |
| Deep Learning | TensorFlow / Keras |
| Data Processing | Pandas, NumPy |
| Frontend | HTML, CSS, JavaScript |
| Weather | OpenWeather API |
| Data Storage | CSV, JSON |
| Model Serialization | Pickle |
| Version Control | Git, GitHub |

---

## 📂 Project Structure

```text
CropPilot/
│
├── app.py
├── train_crop_model.py
├── train_model.py
├── Crop_recommendation.csv
│
├── data/
│   ├── Data.json
│   ├── commodity_price.csv
│   ├── data.csv
│   ├── nutrition.json
│   ├── Train/
│   └── Test/
│
├── models/
│   ├── class_indices.json
│   └── training_hist.json
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── crop.html
│   ├── disease.html
│   ├── market.html
│   ├── weather.html
│   ├── calendar.html
│   └── nutrition.html
│
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shwetagg17/CropPilot.git
cd CropPilot
```

### 2. Create a virtual environment

**Windows**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Install the packages used by the application:

```bash
pip install flask numpy pandas requests scikit-learn tensorflow pillow werkzeug
```

Or, if you add a `requirements.txt` file to the project:

```bash
pip install -r requirements.txt
```

### 4. Configure the weather API key

Set the API key as an environment variable rather than committing secrets to GitHub.

**Windows PowerShell**

```powershell
$env:WEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY"
```

**macOS / Linux**

```bash
export WEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY"
```

### 5. Add required trained model files

The current application code expects these trained artifacts:

```text
crop_model.pkl
scaler.pkl
label_encoder.pkl
models/trained_plant_disease_model.keras
```

These model artifacts are **not currently present in the GitHub repository**, so add them locally or generate them using the project's training scripts before running the complete prediction workflow.

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔗 Application Routes

| Route | Purpose |
|---|---|
| `/` | CropPilot homepage |
| `/crop` | Crop recommendation page |
| `/disease` | Plant disease detection page |
| `/market` | Market trends page |
| `/weather_page` | Weather page |
| `/calendar` | Crop calendar |
| `/nutrition` | Crop nutrition |
| `/predict` | Crop prediction API |
| `/predict_disease` | Disease prediction API |
| `/weather` | City weather API |
| `/weather_by_coords` | Coordinate-based weather API |
| `/market_data` | Crop market-data API |
| `/crop_nutrition` | Crop nutrition API |

---

## 🔐 Security Notes

Before deploying CropPilot publicly:

- **Never commit API keys or other secrets to GitHub.**
- Store the OpenWeather API key in environment variables.
- Rotate any API key that has previously been exposed in source code.
- Validate uploaded image type and size.
- Use a production WSGI server instead of Flask's development server.
- Set appropriate upload limits and sanitize uploaded filenames.
- Disable `debug=True` in production.
- Review CORS, rate limiting, error handling, and authentication before exposing APIs publicly.

---

## 📈 Future Enhancements

- 📍 Automatic location detection
- 🏪 Nearby mandi recommendations
- 💰 Crop profit and ROI calculator
- 📊 Regional crop trends
- 🔔 Farming alerts and notifications
- 👨‍🌾 Farmer community and expert support
- 🤖 AI farming assistant/chatbot
- 📱 Mobile/PWA version
- ☁️ Production cloud deployment
- 🔒 Authentication and role-based access
- 📡 More real-time agricultural data integrations

---

## 🎯 Project Objective

CropPilot brings multiple agricultural utilities into one application so that users can explore:

**Soil → Crop → Plant Health → Weather → Market → Nutrition → Planning**

The project demonstrates the practical use of **Python, Flask, machine learning, deep learning, APIs, data processing, and responsive web development** in an agricultural technology use case.

---

## 👩‍💻 Author

**Shweta Aggarwal**

MCA | Data Analytics | AI/ML

GitHub: https://github.com/Shwetagg17

---

## ⭐ Repository

If you find CropPilot useful, consider giving the project a ⭐ on GitHub.

**Repository:** https://github.com/Shwetagg17/CropPilot
