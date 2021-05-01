from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():
        # NOTE: you should not use your apikey in plain text consider using iam_token directly in PROD enviroments.
        API_KEY = "j_iFO1lfw14_IltudzUFHu-2IElu32oM1ip1pzsJTb77"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]
        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + "eyJraWQiOiIyMDIxMDQyMDE4MzYiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NjIwMDFWM1FSIiwiaWQiOiJJQk1pZC02NjIwMDFWM1FSIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiODA3NjZlYjctMTRlOS00OGU0LWI2MGItMTAxMzA4NTkxNDFkIiwiaWRlbnRpZmllciI6IjY2MjAwMVYzUVIiLCJnaXZlbl9uYW1lIjoiU2FudGlhZ28iLCJmYW1pbHlfbmFtZSI6IlJpb3MiLCJuYW1lIjoiU2FudGlhZ28gUmlvcyIsImVtYWlsIjoic2FudGlhZ28ucmlvc29AdWRlYS5lZHUuY28iLCJzdWIiOiJzYW50aWFnby5yaW9zb0B1ZGVhLmVkdS5jbyIsImF1dGhuIjp7InN1YiI6InNhbnRpYWdvLnJpb3NvQHVkZWEuZWR1LmNvIiwiaWFtX2lkIjoiaWFtLTY2MjAwMVYzUVIiLCJuYW1lIjoiU2FudGlhZ28gUmlvcyIsImdpdmVuX25hbWUiOiJTYW50aWFnbyIsImZhbWlseV9uYW1lIjoiUmlvcyIsImVtYWlsIjoic2FudGlhZ28ucmlvc29AdWRlYS5lZHUuY28ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiYTQ5OGQ4N2I1YWJmNGM1Zjg0NzMzNWM2ZjA1MGY5NzMiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE2MTk4OTc0NTUsImV4cCI6MTYxOTkwMTA1NSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9vaWRjL3Rva2VuIiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.Ve8gO8RrjWBOefykw3HTenNkbyODAV_xFtL2NpKAlW069q1i3_pcnrCKW6ypNNMMZxJNo3BeTIQg51wZRs7bn6jhe2_8Y7ctKx_cHVn6EztkR4124wZoVKOd0trvoc2w5a9USDltLHNvFC-Px5jV48zwJ5NiWBWGxxqUP1hzyWf3rb0BfE2iMum89-NdS5EKpE_n_DObDD4DLuow7ARIwtSQ-iie5sI7WREn7SWNh-50NRc-eAKk1guNXAYOAjuWeUwvCUdA2Zms0e7zblICQSEutSkB5A1v8rfgB0CuP7yv3zKPwxfPv7IfgWvtUU_-NfonQaqastCi622VcgzW5Q"}

        if(form.MesVencimiento.data == None): 
          python_object = []
        else:
          form.Unnamed=1
          python_object = [form.Unnamed.data,form.Cliente.data, form.Pais.data,form.Moneda.data,form.Unidad.data, 
            form.MesVencimiento.data,form.Monto.data, form.plazo.data,float(form.Prob_D.data)]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields":    ["Unnamed: 0",
				"Cliente",
				"Pais",
				"Moneda",
				"Unidad",
				"MesVencimiento",
				"Monto",
				"plazo",
				"Prob_D"], "values": userInput }]}

        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/37264cc6-49e9-496a-bf4e-a955f07affe4/predictions?version=2021-05-01", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)
        if roundedCharge == 1 :
          respuesta="Si entrara en default"
        else: 
          respuesta="Es probable que no entre en default"
        form.abc = respuesta # this returns the response back to the front page
        form.ammount=form.Prob_D.data*form.Monto.data
        return render_template('index.html', form=form)