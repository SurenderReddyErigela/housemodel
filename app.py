from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model from disk
model = joblib.load('house_price_prediction_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    try:
        # Convert the input JSON to a DataFrame with an index to mimic the original DataFrame structure
        input_df = pd.DataFrame([data])
        
        # Ensure DataFrame columns order matches the order expected by the model
        input_df = input_df[['OverallQual', 'YearBuilt', 'TotalBsmtSF', 'GrLivArea']]

        # Make prediction using model loaded from disk as per the data
        prediction = model.predict(input_df)

        # Take the first value of prediction
        output = prediction[0]

        # Create response data
        response_data = {"predicted_price": output}

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/', methods=['GET'])
def home():
    return "House Price Prediction API is running!"

if __name__ == "__main__":
    app.run(debug=True)