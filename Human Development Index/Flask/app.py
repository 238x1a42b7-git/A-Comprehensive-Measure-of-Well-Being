from flask import Flask, request, render_template_string
import pickle
import numpy as np
import os

app = Flask(__name__)

# Track and load model relative to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'HDI.pkl')

try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    print(f"Error: Model file 'HDI.pkl' not found at {model_path}")
    model = None

# EMBEDDED FORM PAGE TEMPLATE (Replaces home.html completely with pristine styling)
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Human Development Index</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: radial-gradient(circle, #0b1e36 0%, #030a16 100%);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        
        h1 {
            color: #ff4d4d;
            font-size: 36px;
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }

        .dashboard-container {
            background: rgba(13, 27, 42, 0.85);
            border: 2px solid #0056b3;
            border-radius: 30px;
            padding: 40px;
            width: 450px;
            box-shadow: 0 0 25px rgba(0, 123, 255, 0.3);
            box-sizing: border-box;
        }

        .form-group {
            margin-bottom: 20px;
            width: 100%;
        }

        select, .form-input {
            width: 100%;
            padding: 12px 20px;
            border-radius: 25px;
            border: 1px solid #00bfff;
            background-color: rgba(255, 255, 255, 0.9);
            color: #333333;
            font-size: 14px;
            box-sizing: border-box;
            text-align: center;
            outline: none;
        }

        select {
            background-color: #ffffff;
            cursor: pointer;
        }

        .btn-predict {
            width: 100%;
            padding: 14px;
            border-radius: 25px;
            border: none;
            background: linear-gradient(90deg, #3a7bd5, #3a6073);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s ease;
            margin-top: 10px;
        }

        .btn-predict:hover {
            background: linear-gradient(90deg, #3a6073, #3a7bd5);
        }
    </style>
</head>
<body>

    <h1>Human Development Index</h1>

    <div class="dashboard-container">
        <form class="form" action="/predict" method="post">
            
            <div class="form-group">
                <select id="country" name="country" required>
                    <option value="" disabled selected>Select the name of the country</option>
                    <option value="1">Afghanistan</option>
                    <option value="2">Australia</option>
                    <option value="3">Bangladesh</option>
                    <option value="4">Canada</option>
                    <option value="5">China</option>
                    <option value="6">India</option>
                    <option value="7">Turkey</option>
                </select>
            </div>

            <div class="form-group">
                <input class="form-input" type="text" name="life_expectancy" placeholder="Enter life expectancy value..." required>
            </div>

            <div class="form-group">
                <input class="form-input" type="text" name="mean_years_of_schooling" placeholder="Enter mean years of schooling..." required>
            </div>

            <div class="form-group">
                <input class="form-input" type="text" name="gni_per_capita" placeholder="Enter Gross National Income (GNI) per capita..." required>
            </div>

            <div class="form-group">
                <input class="form-input" type="text" name="expected_years_of_schooling" placeholder="Enter expected years of schooling..." required>
            </div>

            <button type="submit" class="btn-predict">Predict</button>
        </form>
    </div>

</body>
</html>
"""

# EMBEDDED RESULT PAGE TEMPLATE
RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HDI Prediction Result</title>
</head>
<body style="background: radial-gradient(circle, #0b1e36 0%, #030a16 100%); padding: 50px; display: flex; justify-content: center; align-items: center; min-height: 80vh;">

    <div class="results-panel" style="background: rgba(15, 23, 42, 0.9); border: 2px solid #ff5722; border-radius: 20px; padding: 40px; text-align: center; max-width: 500px; width: 100%; box-shadow: 0 4px 20px rgba(0,0,0,0.5); font-family: Arial, sans-serif;">
        
        <h2 style="color: #ff5722; font-size: 32px; margin-bottom: 5px; font-weight: bold; letter-spacing: 0.5px;">
            Human Development Index
        </h2>
        
        <p style="color: #a0aec0; font-size: 14px; margin-top: 0; margin-bottom: 30px; font-style: italic;">
            A Machine Learning web Application using flask
        </p>

        <div style="color: #ffeb3b; font-size: 26px; font-weight: bold; margin-top: 20px; letter-spacing: 0.5px; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
            {{ category_text }}: HDI {{ prediction_text }}
        </div>
        
        <br><br>
        <a href="/" style="color: #007bff; text-decoration: none; font-weight: bold; font-size: 16px;">&larr; Go Back & Predict Again</a>
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    # Safely renders the form interface using string injection
    return render_template_string(HOME_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Server Error: Model file missing or unreadable.", 500
        
    try:
        features = [
            float(request.form.get('life_expectancy', 0) or 0),
            float(request.form.get('mean_years_of_schooling', 0) or 0),
            float(request.form.get('gni_per_capita', 0) or 0),
            float(request.form.get('expected_years_of_schooling', 0) or 0)
        ]
        
        final_features = np.array([features])
        prediction = model.predict(final_features)
        
        raw_score = float(np.array(prediction).item())
        
        # Scale score correctly into a decimal
        if raw_score > 1.0:
            score = round(raw_score / 100, 2)
        else:
            score = round(raw_score, 2)
            
        score = max(0.0, min(1.0, score))
        
        if score >= 0.80:
            category = "Very High"
        elif score >= 0.70:
            category = "High"
        elif score >= 0.55:
            category = "Medium"
        else:
            category = "Low"
            
        return render_template_string(RESULT_TEMPLATE, 
                                      prediction_text=str(score), 
                                      category_text=category)
                               
    except Exception as e:
        return f"Prediction processed into an error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)