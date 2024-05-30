from flask import Flask,render_template,redirect,url_for,request,jsonify
import pandas as pd
import json
import requests
import joblib

app=Flask(__name__)

data=pd.read_csv('Deep Learning/IPL Score/ipl_data.csv')
venue_encoder=joblib.load('Deep Learning/IPL Score/python_objects/venue_encoder.pkl')
batting_encoder=joblib.load('Deep Learning/IPL Score/python_objects/batting_team_encoder.pkl')
bowling_encoder=joblib.load('Deep Learning/IPL Score/python_objects/bowling_team_encoder.pkl')
striker_encoder=joblib.load('Deep Learning/IPL Score/python_objects/striker_encoder.pkl')
bowler_encoder=joblib.load('Deep Learning/IPL Score/python_objects/bowler_encoder.pkl')
    
encoded_venue=venue_encoder.transform([data['venue'].unique().tolist()][0])
encoded_batting_team=batting_encoder.transform([data['bat_team'].unique().tolist()][0])
encoded_bowling_team=bowling_encoder.transform([data['bowl_team'].unique().tolist()][0])
encoded_striker=striker_encoder.transform([data['batsman'].unique().tolist()][0])
encoded_bowler=bowler_encoder.transform([data['bowler'].unique().tolist()][0])
venue_dict=list(zip(data['venue'].unique().tolist(),encoded_venue))
batting_dict=list(zip(data['bat_team'].unique().tolist(),encoded_batting_team))
bowling_dict=list(zip(data['bowl_team'].unique().tolist(),encoded_bowling_team))
striker_dict=list(zip(data['batsman'].unique().tolist(),encoded_striker))
bowler_dict=list(zip(data['bowler'].unique().tolist(),encoded_bowler))

@app.route('/')
def home():
    return render_template("home.html",venues=venue_dict,batting=batting_dict,bowling=bowling_dict,strikers=striker_dict,bowlers=bowler_dict)
    
@app.route('/predicted',methods=['GET','POST'])
def predict():
    global batting_dict,bowling_dict
    venue=int(request.form.get('venue'))
    batting_team=int(request.form.get('batting_team'))
    bowling_team=int(request.form.get('bowling_team'))
    striker=int(request.form.get('striker'))
    bowler=int(request.form.get('bowler'))
    
    data={'venue':venue,'batting':batting_team,'bowling':bowling_team,'striker':striker,'bowler':bowler}
    url='http://127.0.0.1:8888/receive_data'
    response=requests.post(url,json=data)
    result=response.json()  
    
    batting_team_name=None
    bowling_team_name=None
    for i in range(0,len(batting_dict)):
        if batting_dict[i][1]==batting_team:
            batting_team_name=batting_dict[i][0]
        if bowling_dict[i][1]==bowling_team:
            bowling_team_name=bowling_dict[i][0]
    return render_template('score.html',team1=batting_team_name,team2=bowling_team_name,score=result['score'])
    
app.run(debug=True,port=5000)