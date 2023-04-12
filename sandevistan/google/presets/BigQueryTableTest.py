import os
from constructs import Construct
from sandevistan.providers.GoogleProvider import GoogleProvider
from sandevistan.providers.NullProvider import NullProvider
from sandevistan.google.components.BigQueryTable import BigQueryTable
from sandevistan.null.components.NullResource import NullResource
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

class BigQueryTableTest():
    def __init__(
        self, 
        scope: Construct, 
        stack_name: str,
        project: str,
        location: str,
        service_account_key_path: str,
        dataset_prod: str = None,
        dataset_dev: str = None,
        table_name: str = None
    ):

        self.service_account_key_path = service_account_key_path
        self.scope = scope
        self.stack_name = stack_name
        self.project = project
        self.location = location
        self.dataset_prod = dataset_prod
        self.dataset_dev = dataset_dev
        self.table_name = table_name

        self.add_gcp_provider()

        last_dependency = None

        client = bigquery.Client()

        try:
            table = client.get_table('{}.{}.{}'.format(project, dataset_dev, table_name))
        except NotFound:
            
            table = client.get_table('{}.{}.{}'.format(project, dataset_prod, table_name))

        table_schema_str = self.get_table_schema(table.schema)

        bigquery_table = self.add_bigquery_table(table, table_schema_str)

        last_dependency = bigquery_table

        self.add_null_provider()

        null_resource = self.add_null_resource(depends_on=[last_dependency])

        null_resource.add_override(
            "provisioner.local-exec.command", 
            f'python {os.path.join(os.path.abspath("./"), "sandevistan", "scripts", "insert_data_bq.py")} {self.project} {self.dataset_dev} {self.dataset_prod} {self.table_name} {os.path.abspath(self.service_account_key_path)}'
        )

    def add_gcp_provider(self):
        return GoogleProvider(
            self.scope,
            credentials=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
            project=self.project,
            region=self.location
        )
 
    def add_null_provider(self):
        return NullProvider(
            self.scope,
            id=self.stack_name + '_' + self.table_name + '_null_provider'
        )

    def add_bigquery_table(self, table, table_schema_str, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return BigQueryTable(
                self.scope,
                'bq_test_table_' + self.table_name,
                dataset_id=self.dataset_dev,
                table_id=self.table_name,
                description=table.description,
                schema=table_schema_str,
                deletion_protection=False,
                depends_on=depends_on
            )

    def add_null_resource(self, depends_on=None): 
        depends_on = None if depends_on == [None] else depends_on
        return NullResource(
            self.scope,
            id='insert_data_into_bq_for_' + self.table_name,
            depends_on=depends_on
        )

    def get_table_schema(self, schema):
        table_schema_str = '['

        for field in schema:
            table_schema_str += '{'
            table_schema_str += '"name":"'
            table_schema_str += str(field.name)
            table_schema_str += '","type":"'
            table_schema_str += str(field.field_type)
            table_schema_str += '","mode":"'
            table_schema_str += str(field.mode)
            table_schema_str += '","description":"'
            table_schema_str += str(field.description)
            table_schema_str += '"},'
        table_schema_str = table_schema_str[0:-1]
        table_schema_str += ']'

        return table_schema_str
    