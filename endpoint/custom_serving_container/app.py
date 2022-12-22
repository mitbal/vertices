import flask
from flask import Flask, jsonify, request

import pandas as pd
import lightgbm as lgb

def load_model():

    return lgb.Booster(model_file='model.txt')

model = load_model()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json(force=True)

    df = pd.json_normalize(data['instances'])

    pred = model.predict(df.values)

    return jsonify(pred)


@app.route('/health', methods=['GET'])
def health():
    return flask.Response(status=200)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080)
