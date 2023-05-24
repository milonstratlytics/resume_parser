import numpy as np
import pandas as pd
from resume_scoring import predict_resume_scoring
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', output='')

@app.route('/predict', methods=['POST'])
def predict():
    job_title = request.form.get('job_title')
    skill = request.form.get('skill')
    education = request.form.get('education')
    experience = int(request.form.get('experience'))

    result=predict_resume_scoring(job_title,skill,education,experience)

    return render_template('index.html', output='The output is {}'.format(result))

if __name__ == '__main__':
    app.run(debug=True)
