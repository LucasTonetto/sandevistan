import os
import zipfile
import base64
from datetime import datetime
from constructs import Construct
from sandevistan.providers.GoogleProvider import GoogleProvider
from sandevistan.providers.NullProvider import NullProvider
from sandevistan.google.components.BigQueryTable import BigQueryTable
from sandevistan.google.components.CloudFunction import CloudFunction
from sandevistan.google.components.StorageBucketObject import StorageBucketObject
from sandevistan.google.components.PubSubTopic import PubSubTopic
from sandevistan.google.components.CloudSchedulerJob import CloudSchedulerJob
from sandevistan.google.components.SecretManagerSecret import SecretManagerSecret
from sandevistan.google.components.SecretManagerSecretVersion import SecretManagerSecretVersion
from sandevistan.google.components.ProjectIamMember import ProjectIamMember
from sandevistan.null.components.NullResource import NullResource
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

class CloudFunctionScheduled():
    def __init__(
        self, 
        scope: Construct, 
        stack_name: str,
        project: str,
        location: str,
        service_account_key_paht: str,
        cf_name: str,
        cf_code_path_folder:str,
        bucket_name_for_cf_code: str,
        schedule: str = None,
        prod_environment = False,
        create_secret_keys = False,
        cf_runtime: str = 'python39',
        cf_entrypoint: str = 'main',
        cf_timeout: int = 60,
        cf_memory: int = 256,
        environment_variables: dict = {},
        secret_environment_variables: dict = [],
        secret_variables: dict = [],
        dataset_prod: str = None,
        dataset_dev: str = None,
        table_name: str = None,
        create_table_test = False,
        create_pub_sub_topic_trigger = False,
        pubsub_topic_name: str = None,
        pubsub_message_scheduled: str = None
    ):

        self.environment_variables = environment_variables
        self.service_account_key_paht = service_account_key_paht
        self.scope = scope
        self.stack_name = stack_name
        self.project = project
        self.location = location
        self.cf_name = cf_name
        self.cf_code_path_folder = cf_code_path_folder
        self.bucket_name_for_cf_code = bucket_name_for_cf_code
        self.prod_environment = prod_environment
        self.create_secret_keys = create_secret_keys
        self.cf_runtime = cf_runtime
        self.cf_entrypoint = cf_entrypoint
        self.cf_timeout= cf_timeout
        self.cf_memory = cf_memory
        self.environment_variables = environment_variables
        self.secret_environment_variables = secret_environment_variables
        self.dataset_prod = dataset_prod
        self.dataset_dev = dataset_dev
        self.table_name = table_name
        self.create_table_test = create_table_test
        self.create_pub_sub_topic_trigger = create_pub_sub_topic_trigger
        self.pubsub_topic_name = pubsub_topic_name
        self.pubsub_message_scheduled = pubsub_message_scheduled
        self.schedule = schedule
        self.secret_manager_keys = []
        self.secret_key_versions = []

        for secret in secret_variables:
            self.secret_manager_keys.append(
                {
                    'secret_id': secret['key_name'],
                    'replication': secret['replication'] if 'replication' in secret else { 'automatic': True }
                }
            )
            self.secret_key_versions.append(
                {
                    'secret_id': secret['key_name'],
                    'secret_data': secret['data']
                }
            )
            self.secret_environment_variables.append(
                {
                    'key': secret['environment_variable'],
                    'secret': secret["key_name"],
                    'version': 'latest'
                }
            )

        self.set_credentials_keys()

        self.set_cf_environment_variables('table_name', self.table_name)
        self.set_cf_environment_variables('project_id', self.project)

        if(self.prod_environment):
            self.set_cf_environment_variables('dataset', self.dataset_prod)
        else:
            self.set_cf_environment_variables('dataset', self.dataset_dev)

        timestamp_now = datetime.now().strftime('%Y%m%d_%H%M%S')

        self.clear_zip_files(cf_code_path_folder)

        self.zip_cf_code(cf_code_path_folder, timestamp_now)

        self.add_gcp_provider()

        last_dependency = None

        if(self.create_test_table()):

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
                f'python {os.path.join(os.path.abspath("./"), "lib", "insert_data_bq.py")} {self.project} {self.dataset_dev} {self.dataset_prod} {self.table_name} {os.path.abspath(self.service_account_key_paht)}'
            )

            last_dependency = null_resource

        last_dependencies = []

        if(self.create_secret_keys):
            for secret_manager, secret_manager_version in zip(self.secret_manager_keys, self.secret_key_versions):
                secret_manager_resource = self.add_secret_manager(secret_manager['secret_id'], secret_manager['replication'])
                secret_manager_version_resource = self.add_secret_manager_version(
                    secret_manager_version['secret_id'], 
                    secret_manager_resource.id, 
                    secret_manager_version['secret_data'], 
                    depends_on=[secret_manager_resource]
                )
                last_dependencies.append(secret_manager_version_resource)                

        if(self.create_pub_sub_topic_trigger is True):
            pub_sub_topic = self.add_pubsub_topic(depends_on=[last_dependency])
            last_dependency = pub_sub_topic
            pubsub_topic_name = pub_sub_topic.id
            self.add_scheduler(pubsub_topic_name, depends_on=[last_dependency])                  

        if(self.pubsub_topic_name is not None):
            event_trigger_cf_resource = f'projects/{self.project}/topics/{self.pubsub_topic_name}'
        else:
            event_trigger_cf_resource = pubsub_topic_name

        event_trigger_cf = {
            'event_type': 'google.pubsub.topic.publish',
            'resource': event_trigger_cf_resource
        }

        if(len(last_dependencies) > 0):
            dependencies_for_cf = last_dependencies
            dependencies_for_cf.append(last_dependency)
        else:
            dependencies_for_cf = [last_dependency]

        cf_zip_cod_storage = self.input_object_into_storage_bucket(timestamp_now, depends_on=dependencies_for_cf)

        self.add_cloud_function(cf_zip_cod_storage, event_trigger_cf)

    def set_credentials_keys(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(self.service_account_key_paht)

    def set_cf_environment_variables(self, env_var_name, value):
        self.environment_variables[env_var_name] = value
        
    def clear_zip_files(self, cf_code_path_folder):
        for _, _, files in os.walk(cf_code_path_folder):
            for file in files:
                 if '.zip' in file:
                    os.remove(cf_code_path_folder + '/' + file)

    def zip_cf_code(self, cf_code_path_folder, timestamp_now):
        for dirname, _, files in os.walk(cf_code_path_folder):
            with zipfile.ZipFile(cf_code_path_folder + '/cf_code' + timestamp_now + '.zip', mode='w')  as archive:
                    for file in files:
                            if '.zip' not in file:
                                archive.write(dirname + '/' + file, file)

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
            id=self.stack_name + '_' + self.cf_name + '_null_provider'
        )

    def create_test_table(self):
        if (self.prod_environment is False and self.create_table_test is True and (self.dataset_dev is None or self.table_name is None)):
            raise Exception('Parâmetros incorretos! Para criar a copia da tabela no dataset de testes é necessário informar o nome do dataset de teste e a tabela')
        return (self.create_table_test is True and self.prod_environment is False)
    
    def add_bigquery_table(self, table, table_schema_str, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return BigQueryTable(
                self.scope,
                dataset_id=self.dataset_dev,
                table_id=self.table_name,
                description=table.description,
                id_='bq_test_table_for_' + self.cf_name,
                schema=table_schema_str,
                deletion_protection=False,
                depends_on=depends_on
            )

    def add_null_resource(self, depends_on=None): 
        depends_on = None if depends_on == [None] else depends_on
        return NullResource(
            self.scope,
            id='insert_data_into_bq_for_' + self.cf_name,
            depends_on=depends_on
        )

    def add_pubsub_topic(self, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return PubSubTopic(
            self.scope,
            'pub_sub_for_cf_' + self.cf_name,
            'pub_sub_for_cf_' + self.cf_name,
            depends_on=depends_on
        )

    def add_secret_manager(self, secret_id, replication):
        return SecretManagerSecret(
            self.scope,
            secret_id,
            secret_id,
            replication=replication
        )

    def add_secret_manager_version(self, secret_name, secret_id, secret_data, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return SecretManagerSecretVersion(
            self.scope,
            'version_for_' + secret_name,
            secret_id,
            secret_data,
            depends_on=depends_on
        )
    
    def input_object_into_storage_bucket(self, timestamp, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return StorageBucketObject(
            self.scope,
            'bucket_for_cf_' + self.cf_name + '_code',
            bucket=self.bucket_name_for_cf_code,
            name=self.cf_name + '_code.zip',
            source=os.path.abspath(self.cf_code_path_folder + '/cf_code' + timestamp + '.zip'),
            depends_on=depends_on
        )

    def add_cloud_function(self, cf_zip_cod_storage, event_trigger_cf):
        return CloudFunction(
            self.scope,
            self.cf_name,
            name=self.cf_name,
            runtime=self.cf_runtime,
            available_memory_mb=self.cf_memory,
            source_archive_bucket=self.bucket_name_for_cf_code,
            source_archive_object=cf_zip_cod_storage.name,
            timeout=self.cf_timeout,
            entry_point=self.cf_entrypoint,
            environment_variables=self.environment_variables,
            depends_on=[cf_zip_cod_storage],
            event_trigger=event_trigger_cf,
            secret_environment_variables=self.secret_environment_variables
        )

    def add_scheduler(self, pubsub_topic_name, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return CloudSchedulerJob(
            self.scope,
            'scheduler_for_cf_' + self.cf_name,
            self.schedule,
            pubsub_target={
                'topic_name': pubsub_topic_name,
                'data': self.pubsub_message_scheduled
            },
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
    