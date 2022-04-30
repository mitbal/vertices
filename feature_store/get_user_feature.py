import json
import requests
import subprocess

from google.cloud import aiplatform as vertex

REGION = 'us-central1'
PROJECT_ID = 'mitochondrion-project-344303'
ENDPOINT_ID = '8823932656623288320'

URL = f'https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict'

def handle_request(user_id):

    vertex.init(project=PROJECT_ID, location='asia-southeast1')

    user_entity_type = vertex.featurestore.EntityType(
    entity_type_name='users', featurestore_id='marketing_featurestore')

    serving_df = user_entity_type.read(
        entity_ids=[user_id],
        feature_ids=['channel', 'history', 'zip_code'],
    )

    serving_df['history'] = serving_df['history'].astype('str')

    payload = {
        'instances': [
            serving_df.loc[0, 'channel':].to_dict()
        ]
    }

    out = subprocess.run('gcloud auth application-default print-access-token'.split(), 
        capture_output=True, text=True)
    access_token = out.stdout

    r = requests.post(URL, data=json.dumps(payload), headers={'Authorization': f'Bearer {access_token.strip()}'})

    response = json.loads(r.text)
    print(response)
    return response

handle_request('UID2733')
