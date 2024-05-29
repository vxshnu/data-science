from flask import Flask,render_template,redirect,url_for,request
import pandas as pd
app=Flask(__name__)

data=pd.read_csv('ipl_data.csv')

@app.route('/')
def home():
    return render_template('home.html',venues=data['venue'].unique().tolist(),batting=data['bat_team'].unique().tolist(),bowling=data['bowl_team'].unique().tolist(),strikers=data['batsman'].unique().tolist(),bowlers=data['bowler'].unique().tolist())

@app.route('/predicted',methods=['POST'])
def predict():
    venue=request.form.get('venue')
    batting_team=request.form.get('batting_team')
    bowling_team=request.form.get('bowling_team')
    striker=request.form.get('striker')
    bowler=request.form.get('bowler')
    
    
app.run(debug=True)