from flask import Flask,jsonify,request

app = Flask(__name__)

import pandas as pd


@app.route('/',methods = ['GET','POST'])
def ratingReturn():
    df = pd.read_csv("BS_NEW.csv")
    request_data = request.get_json()
    rating = request_data['Rating']
    df = df[(df['Problem Rating'] == rating - 100) | (df['Problem Rating'] == rating)]
    return jsonify({'Problem Number': df.sample(1)['Problem Number'].to_list()[0],'Problem Statement': df.sample(1)['Problem Statement'].to_list()[0],'Input Format': df.sample(1)['Input Specifications'].to_list()[0],'Output Format':  df.sample(1)['Output Specifications'].to_list()[0]})
