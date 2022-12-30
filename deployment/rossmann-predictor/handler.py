import pickle
import os
import pandas as pd
from flask import Flask, request, Response, abort
from rossmann.Rossmann import Rossmann

# Loading model
model = pickle.load(open('model/tuned_xgb_rossmann.pkl', 'rb'))

# Initializing API
app = Flask(__name__)

# API endpoint
@app.route('/rossmann/predict', methods=['POST'])    

def rossmann_predict():
    if request.method == 'POST':
        test_json = request.get_json()
        
        if test_json: # There's data
            if isinstance(test_json, dict): # Unique example
                test_raw = pd.DataFrame(test_json, index=[0])
            else: # Multiple example
                test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
        
            # Instantiate class
            pipeline = Rossmann()
        
            # Cleaning
            df1 = pipeline.data_cleaning(test_raw)
            # Feature engineering
            df2 = pipeline.feature_engineering(df1)
            # Preparation
            df3 = pipeline.data_preparation(df2)
            # Prediction
            df_response = pipeline.get_prediction(model, test_raw, df3)
        
            return df_response

        else: # Empty
            return Response('{}', status=200, mimetype='application/json')
    else:
        abort(405)
    
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)