import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, render_template, jsonify 

app = Flask('readmorecanlit')

@app.route('/')

def form():
	return render_template('index.htm')

@app.route('/submit')

def submit():
	user_input = request.args
	data = [user_input['recommender-input']]

	model = pickle.load(open('models/model.p', 'rb'))

	system_recommendation = 'recommendation command'

	return render_template('recommendation.htm', system_recommendation)
	# return jsonify({'data': data})



if __name__ == '__main__':   # means 'if script is running from terminal'
	app.run(debug=True)