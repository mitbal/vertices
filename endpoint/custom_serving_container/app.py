import flask
from flask import Flask, jsonify, request

import numpy as np
import lightgbm as lgb

def load_model():

    return lgb.Booster(model_file='model.txt')

model = load_model()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json(force=True)

    X = np.array(data['instances'])
    pred = model.predict(X)

    return jsonify(pred.tolist())


@app.route('/health', methods=['GET'])
def health():
    return flask.Response(status=200)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080)
