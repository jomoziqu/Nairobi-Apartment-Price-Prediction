from flask import Flask, render_template, request, jsonify
import joblib 
import numpy as np
import xgboost as xgb
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Load the trained model 
model = joblib.load('model/xgboost_model.pkl')


location_names = {
    0: "Ruaka",
    1: "Utawala",
    2: "Kileleshwa",
    3: "Lavington",
    4: "Westlands",
    5: "Ruiru",
    6: "Juja",
    7: "Syokimau",
    8: "Muthaiga",
    9: "Kilimani"
}


@app.route('/')
def home():
    # Render the HTML template for the home page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input data from the form (JSON format)
    data = request.json
    location = int(data['location'])
    distance = float(data['distance'])
    bedrooms = int(data['bedrooms'])
    bathrooms = int(data['bathrooms'])
    floor_size = float(data['floor_size'])
    amenities = [int(amenity) for amenity in data['amenities']]

    # Prepare the input data for the model 
    input_data = [location, distance, bedrooms, bathrooms, floor_size] + amenities


    input_dict = dict(zip(model.feature_names, input_data))
    input_df = pd.DataFrame([input_dict])
    

    # Convert the pandas DataFrame to a DMatrix object 
    dmatrix = xgb.DMatrix(input_df)
    
    # Make prediction using the model
    price = model.predict(dmatrix)
    predicted_price = round(price.item(), 0)

    # Get the location name based on the location ID
    location_name = location_names.get(location, "Unknown Location")

    return jsonify({
        'predicted_price': predicted_price,
        'location_name': location_name
    }) 

if __name__ == '__main__':
    app.run(debug=True)
