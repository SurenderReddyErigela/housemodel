from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os

app = Flask(__name__, static_folder='build', static_url_path='')

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    # When running locally, disable this if you don't want to use the React build
    # app.run(debug=True, use_reloader=True)
    # When running on Heroku, comment out the above line and uncomment the below line
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
