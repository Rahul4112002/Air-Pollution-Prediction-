from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import matplotlib
from sklearn.preprocessing import StandardScaler
application = Flask(__name__)
app=application
model = pickle.load(open('pickle_model.pickle', 'rb'))
@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')
@app.route('/home.html', methods=['GET'])
def home():
    return render_template('home.html')



standard_to = StandardScaler()
@app.route('/form.html', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'POST':
        COAQIValue = int(request.form['COAQIValue'])
        COAQICategory = int(request.form['COAQICategory'])
        OzoneAQIValue = int(request.form['OzoneAQIValue'])
        OzoneAQICategory = float(request.form['OzoneAQICategory'])
        NO2AQIValue = int(request.form['NO2AQIValue'])
        NO2AQICategory = int(request.form['NO2AQICategory'])
        PM25AQIValue = int(request.form['PM25AQIValue'])
        PM25AQICategory = float(request.form['PM25AQICategory'])
        
        prediction_value = model.predict([[COAQIValue, COAQICategory, OzoneAQIValue, OzoneAQICategory, NO2AQIValue, NO2AQICategory, PM25AQIValue, PM25AQICategory]])[0]
        
        if prediction_value <= 50:
            prediction_text = "Good "
            prediction_text2 = "The air quality is generally acceptable; there are little to no health risks associated with the air quality at this level."
        elif prediction_value <= 100:
            prediction_text = "Moderate"
            prediction_text2 = "Suggests that the air quality is acceptable, but there may be some pollutants present that could pose a moderate health concern for a very small number of people who are sensitive to air pollution.."
        elif prediction_value <= 150:
            prediction_text = "Unhealthy for Sensitive Groups "
            prediction_text2 = "Indicates that the air quality may pose health concerns for individuals who are particularly sensitive to air pollution, such as those with respiratory conditions or the elderly. "
        elif prediction_value <= 200:
            prediction_text = "Unhealthy"
            prediction_text2 = "  Signifies that the air quality is unhealthy, and everyone may begin to experience adverse health effects. People with respiratory or heart conditions, children, and the elderly are particularly at risk."
        elif prediction_value <= 300:
            prediction_text = "Very Unhealthy"
            prediction_text2 = "Indicates that the air quality is very poor and may pose serious health risks to the entire population. People are advised to limit outdoor activities and take precautions to protect their health. "
        else:
            prediction_text = "Hazardous  "
            prediction_text2 = "Signifies that the air quality is extremely poor, with severe health effects expected for everyone. Outdoor activities should be avoided, and individuals are advised to stay indoors and use air purifiers if available."
        return render_template('form.html', prediction_value=prediction_value, prediction_text=prediction_text , prediction_text2=prediction_text2)

        
    return render_template('form.html')        
if __name__=="__main__":
    app.run(debug=True)