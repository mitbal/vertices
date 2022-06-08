from google.cloud import aiplatform

job = aiplatform.PipelineJob(
    display_name = PIPELINE_NAME,
    # template_path = JSON_FILE,
    template_path = 'gs://mitochondrion-bucket-sg/marketing/marketing_custom_pipeline.json',
    enable_caching = True,
    project = PROJECT_ID,
    location = REGION,
    parameter_values = {
        'current_date': '2022-02-05'
    }
)

# job.submit()
job.submit(service_account='default@mitochondrion-project-344303.iam.gserviceaccount.com')

