import kfp
from kfp.v2 import compiler
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics

PROJECT_ID = 'mitochondrion-project-344303'
REGION = 'asia-southeast1'

BUCKET_NAME = 'gs://mitochondrion-bucket-sg'
PIPELINE_ROOT = f'{BUCKET_NAME}/pipelines'
PIPELINE_NAME = 'marketing-custom-pipeline'

@component(base_image='google/cloud-sdk:latest',
            packages_to_install=['pandas==1.3.4',
                                'pandas-gbq==0.17.4',
                                'google-cloud-bigquery==2.34.2'
            ]
)
def get_latest_data_from_bq(train_dataset: Output[Dataset],
                               test_dataset: Output[Dataset],
                               current_date: str = '2022-01-01'):

    from datetime import datetime, timedelta
    import pandas as pd

    start_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=7*4)).strftime('%Y-%m-%d')
    end_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')

    query = """
        SELECT
        *
        FROM
        `mitochondrion-project-344303.dataset.marketing`
        WHERE
        created_date >= '{start_date}'
        AND created_date <= '{current_date}'
    """.format(start_date=start_date, current_date=current_date)

    df = pd.read_gbq(query, project_id='mitochondrion-project-344303', dialect='standard')

    train_df = df[(df['created_date'] >= start_date) & (df['created_date'] <= end_date)]
    test_df = df[df['created_date'] == current_date]

    train_df.to_csv(train_dataset.path, index=False)
    test_df.to_csv(test_dataset.path, index=False)

@component(base_image='python:3.9.12',
            packages_to_install=['pandas==1.3.4',
                                'scikit-learn==1.0.2',
            ]
)
def transform_feature(raw_dataset: Input[Dataset],
                        transformed_dataset: Output[Dataset]):

    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import OneHotEncoder

    df = pd.read_csv(raw_dataset.path)

    std = StandardScaler()
    std.fit(df[['history']])
    transformed_df = pd.DataFrame(std.transform(df[['history']]), columns=['history_std'])

    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit(df[['zip_code', 'channel', 'offer']])
    transformed_df[enc.get_feature_names_out(['zip_code', 'channel', 'offer'])] = enc.transform(df[['zip_code', 'channel', 'offer']]).toarray()

    transformed_df[['used_bogo', 'used_discount', 'is_referral', 'conversion']] = df[['used_bogo', 'used_discount', 'is_referral', 'conversion']]

    transformed_df.to_csv(transformed_dataset.path, index=False)

train_xgboost_model = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/mitbal/vertices/main/component/xgboost_training/component.yaml')

@component(base_image='google/cloud-sdk:latest',
            packages_to_install=['pandas==1.3.4',
                                'pandas-gbq==0.17.4',
                                'google-cloud-bigquery==2.34.2',
                                'xgboost==1.5.1',
                                'scikit-learn==1.0.2',
            ]
)
def create_batch_prediction(
                            dataset: Input[Dataset],
                            model_artifact: Input[Model],
                            predictions_dataset: Output[Dataset],
                            current_date: str = '2022-01-01'
):

    import pickle
    import pandas as pd
    from xgboost.sklearn import XGBClassifier

    model = pickle.load(open(model_artifact.path, 'rb'))

    data = pd.read_csv(dataset.path)
    X = data.drop('conversion', axis=1).values
    predictions = model.predict(X)

    predictions_df = pd.DataFrame({'prediction': predictions})
    predictions_df['prediction_date'] = current_date
    predictions_df.to_csv(predictions_dataset.path, index=False)

    predictions_df.to_gbq('prediction.marketing', 'mitochondrion-project-344303', if_exists='append')

@pipeline(
    pipeline_root=PIPELINE_ROOT,
    name=PIPELINE_NAME
)
def custom_pipeline(
    current_date: str = '2022-01-01'
):
    dataset = get_latest_data_from_bq(current_date=current_date)
    transformed_train = transform_feature(dataset.outputs['train_dataset'])
    transformed_test = transform_feature(dataset.outputs['test_dataset'])
    model = train_xgboost_model(transformed_train.outputs['transformed_dataset'])
    create_batch_prediction(transformed_test.outputs['transformed_dataset'], model.outputs['model_artifact'], 
                            current_date)

JSON_FILE = '/workspace/marketing_custom_pipeline.json'

compiler.Compiler().compile(
    pipeline_func=custom_pipeline,
    package_path=JSON_FILE
)


