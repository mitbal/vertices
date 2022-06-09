def plus(x, y):
    return x + y

def test_plus():

    assert plus(1, 1) == 2

def test_model():

    import subprocess

    subprocess.call(['python', '../xgboost_training.py', '--dataset', 'testdata.csv', '--model-artifact', 'model.pkl'])

    import pandas as pd
    from xgboost.sklearn import XGBClassifier

    import pickle

    model = pickle.load(open('model.pkl', 'rb'))

    df = pd.read_csv('testdata.csv')
    X = df.drop(['label'], axis=1).values
    y = df.pop('label').values

    assert model.predict(X).tolist() == y.tolist()
