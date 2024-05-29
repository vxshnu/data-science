from flask import Flask,render_template,redirect,url_for,request,jsonify
import pandas as pd
import json
import requests
app=Flask(__name__)

data=pd.read_csv('Deep Learning/IPL Score/ipl_data.csv')

@app.route('/')
def home():
    return render_template('home.html',venues=data['venue'].unique().tolist(),batting=data['bat_team'].unique().tolist(),bowling=data['bowl_team'].unique().tolist(),strikers=data['batsman'].unique().tolist(),bowlers=data['bowler'].unique().tolist())

@app.route('/predicted',methods=['POST'])
def predict():
    venue=request.form.get('venue')
    print("Venu:",venue)
    batting_team=request.form.get('batting_team')
    bowling_team=request.form.get('bowling_team')
    striker=request.form.get('striker')
    bowler=request.form.get('bowler')
    data={'venue':venue,'batting':batting_team,'bowling':bowling_team,'striker':striker,'bowler':bowler}
    #json_data=json.dumps(data)
    json_data=jsonify(data)
    print(json_data)
    url='http://localhost:8888/receive_data'
    #headers = {'Content-Type': 'application/json'}
    response=requests.post(url,data=data)
    print("response:",response)
    result=response.json()
    return render_template('score.html',team1=batting_team,team2=bowling_team,score=result['score'])
    
app.run(debug=True)