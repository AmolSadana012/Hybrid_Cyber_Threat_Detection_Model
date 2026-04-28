# Cloud-Based Architecture
# Flask inference server

from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load Trained Model
try:
    model = joblib.load("cyber_model.pkl")
    print("Model loaded successfully")
except Exception as e:
    print("Error loading model:", e)

@app.route('/')
def home():
    return "Cloud Intrusion Detection Server Running"

# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receive incoming packet features
        data = request.json["features"]
        # Convert to numpy array
        features = np.array(data).reshape(1,-1)
        # Predict
        pred = model.predict(features)[0]
        if pred == 1:
            result = "ATTACK DETECTED "
        else:
            result = "NORMAL TRAFFIC "
        return jsonify({
            "prediction": result
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    print("Starting Flask Server...")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )