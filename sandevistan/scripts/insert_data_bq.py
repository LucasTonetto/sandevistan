import sys
from google.cloud import bigquery
from google.oauth2 import service_account

parameters = sys.argv[1:]

project = parameters[0]
dataset_dev = parameters[1]
dataset_prod = parameters[2]
table_name = parameters[3]
credentials_path = parameters[4]

credentials = service_account.Credentials.from_service_account_file(
    credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)
query = client.query(f'INSERT INTO {project}.{dataset_dev}.{table_name} SELECT * FROM {project}.{dataset_prod}.{table_name}')
query.result()