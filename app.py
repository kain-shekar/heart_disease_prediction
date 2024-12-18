import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

# load the model
model = pickle.load(open('heart_prediction_model','rb'))
scaledFun = pickle.load(open('scaledfun','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])

## function to take values in json format from postman
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scaledFun.transform(np.array(list(data.values())).reshape(1,-1))
    output=model.predict(new_data)
    print(output[0])
    return jsonify(int(output[0]))

# API to take values from the form as input to the model to predict value using predict function
@app.route('/predict', methods=['POST'])

def predict():
    data = [float(x) for x in request.form.values()]
    new_data = scaledFun.transform(np.array(data).reshape(1,-1))
    output = model.predict(new_data)
    print(output[0])
    if output[0] == 0:
      return render_template('home.html',prediction_text="The patient don't have any Heart Disease {}".format(output))
    else :
      return render_template('home.html',prediction_text="The patient  have a Heart Disease {}".format(output))




if __name__ == "__main__":
    app.run(debug=True)


