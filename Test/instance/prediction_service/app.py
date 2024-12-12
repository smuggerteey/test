from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load model and scaler
model = load_model('instance/ml-model-container/ML-models/wmodel.keras')
scaler = joblib.load('instance/ml-model-container/ML-models/scaler.pkl')

# Serve index.html
@app.route('/')
def home():
    return render_template('predictions.html')

# API for prediction
@app.route('/predict_water_availability', methods=['POST'])
def predict_water_availability():
    try:
        data = request.json['data']
        input_array = np.array(data).reshape((1, 1, len(data)))
        predictions = model.predict(input_array).flatten().tolist()
        return jsonify({'predictions': predictions})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
