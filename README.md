# 🌍 Human Development Index Project

Welcome to the Human Development Index (HDI) prediction project! This experience combines data science, machine learning, and web development to estimate a country's development level using important socioeconomic factors.

## ✨ What this project does

This project:
- analyzes human development data from a CSV file
- builds a regression model to predict HDI
- saves the trained model for reuse
- uses a Flask web app to let users make predictions interactively

## 🧠 Project Flow

1. Explore the dataset and understand relationships between variables
2. Train a machine learning model using regression
3. Save the trained model as a pickle file
4. Deploy the model through a simple web interface

## 📁 Project Structure

- Dataset/HDI.csv — the dataset used for training and analysis
- Training/HumDevIndex.ipynb — notebook containing the modeling workflow
- Flask/app.py — Flask application for prediction
- Flask/templates/ — HTML pages for the frontend interface
- Flask/HDI.pkl — trained model file

## 🛠️ Technologies Used

- Python
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- Flask

## 🚀 Getting Started

### Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn flask
```

### Run the notebook
Open and execute:

- Training/HumDevIndex.ipynb

This will train the model and update:

- Flask/HDI.pkl

### Start the web app
Run:

```bash
python Flask/app.py
```

Then open your browser at:

```text
http://127.0.0.1:5000/
```

## 📊 Input Features

The prediction app uses these values:
- Life expectancy
- Mean years of schooling
- Expected years of schooling
- Gross National Income (GNI) per capita

## 🎯 Result

The model predicts an HDI score and classifies it into development categories such as:
- Low
- Medium
- High
- Very High

## 💡 Why it is useful

This project demonstrates how data science and web applications can work together to make predictions accessible and user-friendly.
