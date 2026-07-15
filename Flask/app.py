from flask import Flask, request, render_template
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

@app.route('/')
def home():
    return render_template('home.html')

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
            
        return render_template('index.html', 
                               prediction_text=str(score), 
                               category_text=category)
                               
    except Exception as e:
        return f"Prediction processed into an error: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)