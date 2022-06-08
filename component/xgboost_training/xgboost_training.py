import pickle
import argparse

import pandas as pd
from xgboost.sklearn import XGBClassifier

parser = argparse.ArgumentParser(description="Train XGBoost model")

parser.add_argument('--dataset', type=str, required=True, help='Local or GCS path to the training dataset')
parser.add_argument('--model-artifact', type=str, required=True, help='Local or GCS path to the output model file')
args = parser.parse_args()

df = pd.read_csv(args.dataset)
X = df.drop(['label'], axis=1).values
y = X.pop('label').values

model = XGBClassifier(n_estimator=100, max_depth=3, learning_rate=0.1, silent=True)
model.fit(X, y)

with open(args.model_artifact, 'wb') as f:
    pickle.dump(model, f)

