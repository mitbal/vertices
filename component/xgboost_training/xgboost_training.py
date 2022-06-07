import os
import json
import pickle
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

parser = argparse.ArgumentParser(description="Train XGBoost model")

parser.add_argument('--training-set-features-path', type=str, required=True, help='Local or GCS path to the training dataset')
parser.add_argument('--output-model-path-file', type=str, required=True, help='Local or GCS path to the output model file')

args = parser.parse_args()

df = pd.read_csv(args.training_set_features_path)
X = df.drop(['label'], axis=1).values
y = X.pop('label').values

model = xgb.XGBClassifier(n_estimator=100, max_depth=3, learning_rate=0.1, silent=True)
model.fit(X, y)

with open(args.output_model_path_file, 'wb') as f:
    pickle.dump(model, f)

# Path(args.output_model_path_file).parent.mkdir(parents=True, exist_ok=True)
# Path(args.output_model_path_file).write_text(args.output_model_path)
