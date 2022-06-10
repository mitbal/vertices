def test_fail():

    assert 1 == 2 # this should fail

def test_model():

    import subprocess

    subprocess.call(['python', '../xgboost_training.py', '--dataset', './component/xgboost_training/test/testdata.csv', '--model-artifact', 'model.pkl'])

    import pandas as pd
    from xgboost.sklearn import XGBClassifier

    import pickle

    model = pickle.load(open('./component/xgboost_training/test/model.pkl', 'rb'))

    df = pd.read_csv('./component/xgboost_training/test/testdata.csv')
    X = df.drop(['label'], axis=1).values
    y = df.pop('label').values

    assert model.predict(X).tolist() == y.tolist()
