
from flask_cors import CORS, cross_origin
import numpy as np
from flask import Flask, request, render_template
import joblib
import files.kampanya as kampanya
import pandas as pd
import json
import files.gpt as gpt 





app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = joblib.load("voting_clf.pkl")


@app.route('/predict-ocean',methods=['POST'])
@cross_origin()
def predictOcean():
    #veriyi data.json dosyasına yazdır
    with open('data.json', 'w') as f:
        json.dump(request.json, f)

    #veriyi oku
    df = pd.read_json(r'data.json')
    #model için veriyi düzenle
    df = kampanya.veriyi_duzenle(df)
    data = df

    #müşteri değerlerini al
    musteri_degerleri = kampanya.sum_of_my_question_groups(data, model)
    response=kampanya.kampanya_onerisi(float(musteri_degerleri["cluster"]))
    result={
        "O":float(musteri_degerleri["open"]),
        "C":float(musteri_degerleri["conscientious"]),
        "E":float(musteri_degerleri["extroversion"]),
        "A":float(musteri_degerleri["agreeable"]),
        "N":float(musteri_degerleri["neurotic"]),
    }
    response["results"]=result
    
    return response



@app.route('/ask-to-gpt',methods=['POST'])
@cross_origin()
def askToGpt():
    data=request.json
    
    response=gpt.useGpt(data["prompt"])
    return response


if __name__ == "__main__":
    app.run()