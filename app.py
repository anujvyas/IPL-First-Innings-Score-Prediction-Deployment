# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.form['batting-team']
	bowling_team = request.form['bowling-team']
	
	team_list = ['Chennai Super Kings', 'Delhi Daredevils' ,'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
	batting_temp_array = [0, 0, 0, 0, 0, 0, 0, 0]
	bowling_temp_array = [0, 0, 0, 0, 0, 0, 0, 0]
	
	for i in len(team_list):
		if batting_team == team_list[i]:
			batting_temp_array[i] = 1
		if bowling_team == team_list[i]:
			bowling_temp_array[i] = 1
	temp_array = temp_array + batting_temp_array
	temp_array = temp_array + bowling_temp_array           
            
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])
              
        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)



if __name__ == '__main__':
	app.run(debug=True)
