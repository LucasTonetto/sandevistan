import os
from constructs import Construct

from sandevistan.providers.NullProvider import NullProvider
from sandevistan.null.components.NullResource import NullResource

from sandevistan.providers.GoogleProvider import GoogleProvider
from sandevistan.google.components.ArtifactRegistryRepository import ArtifactRegistryRepository
from sandevistan.google.components.CloudRunJob import CloudRunJob
from sandevistan.google.components.CloudSchedulerJob import CloudSchedulerJob

# Credenciais Docker + GCP > https://cloud.google.com/artifact-registry/docs/docker/authentication?hl=pt-br#standalone-helper

class CloudRunScheduled():
    def __init__(
        self,
        scope: Construct,
        project: str,
        region: str,
        name: str,
        docker_image_name: str,
        service_account_email: str,
        scheduler_cron: str,
        create_repository = False,
        service_account_path = None,
        build_docker_image = False,
        docker_image_to_build_folder_path = None,
        artifact_format = 'DOCKER'
    ):

        self.scope = scope
        self.project = project
        self.region = region
        self.name = name
        self.docker_image_name = docker_image_name
        self.service_account_email = service_account_email
        self.scheduler_cron = scheduler_cron
        self.create_repository = create_repository
        self.service_account = service_account_path
        self.build_docker_image = build_docker_image
        self.docker_image_to_build_folder_path = docker_image_to_build_folder_path
        self.artifact_format = artifact_format

        self.artifact_registry_name = f'{self.name}-sandevistan-repository'
        self.artifact_registry_repository_iam_member_id = f'{self.name}-sandevistan-repository-iam-member'
        self.coud_run_job_name = f'{self.name}-sandevistan-cloud-run-job'
        self.cloud_scheduler_job_name = f'{self.name}-sandevistan-cloud-scheduler-job'

        self.docker_image_url = f'{self.region}-docker.pkg.dev/{self.project}/{self.artifact_registry_name}/{self.docker_image_name}'

        self.add_google_cloud_provider()

        artifacty_registry_repository = None

        if(self.create_repository is True):
            artifacty_registry_repository = self.add_artifact_register_repository()

        resource_push_docker_image = None

        if(self.has_build_docker_image()):
            self.add_null_provider()

            resource_set_google_credentials = self.add_null_resource(
                id=f'{self.name}-set-google-credentials-null_resource',
                provisioners=[
                    {
                        'type': 'local-exec', 
                        'command': f'export GOOGLE_APPLICATION_CREDENTIALS={os.path.abspath(self.docker_image_to_build_folder_path)}'
                    }
                ], 
                depends_on=[artifacty_registry_repository]
            )

            resource_build_docker_image = self.add_null_resource(
                id=f'{self.name}-build-docker-image-null_resource',
                provisioners=[
                    {
                        'type': 'local-exec', 
                        'command': f'docker build -t {self.docker_image_name} {os.path.abspath(self.docker_image_to_build_folder_path)}/'
                    }
                ], 
                depends_on=[resource_set_google_credentials]
            )

            resource_put_docker_tag = self.add_null_resource(
                id=f'{self.name}-put-docker-tag-null_resource',
                provisioners=[
                    {
                        'type': 'local-exec', 
                        'command': f'docker tag {self.docker_image_name} {self.docker_image_url}'
                    }
                ], 
                depends_on=[resource_build_docker_image]
            )

            resource_push_docker_image = self.add_null_resource(
                id=f'{self.name}-push-docker-image-null_resource',
                provisioners=[
                    {
                        'type': 'local-exec', 
                        'command': f'docker push {self.docker_image_url}'
                    }
                ], 
                depends_on=[resource_put_docker_tag]
            )

        cloud_run_template = self.build_cloud_run_template()

        cloud_run_depends_on = resource_push_docker_image if resource_push_docker_image is not None else artifacty_registry_repository

        cloud_run_job = self.add_cloud_run_job(cloud_run_template, depends_on=[cloud_run_depends_on])

        http_target = self.build_http_target_trigger()

        self.add_cloud_scheduler_job(http_target, depends_on=[cloud_run_job])

    def add_google_cloud_provider(self):
        return GoogleProvider(
            self.scope, 
            credentials=os.path.abspath(self.service_account),
            project=self.project,
            region=self.region
        )

    def add_artifact_register_repository(self):
        return ArtifactRegistryRepository(self.scope, self.artifact_registry_name, self.region, format=self.artifact_format)

    def has_build_docker_image(self):
        return True if self.build_docker_image is True and \
            self.docker_image_name is not None and \
            self.docker_image_to_build_folder_path is not None \
            else False

    def add_null_provider(self):
        return NullProvider(
            self.scope,
            id=f'{self.name}-null_provider'
        )

    def add_null_resource(self, id, provisioners, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return NullResource(
            self.scope,
            id=id,
            provisioners=provisioners,
            depends_on=depends_on
        )

    def build_cloud_run_template(self):
        return {
            "labels": { "cdktf-sandevistan": self.scope.name },
            "template": {
                "containers": [
                    { 
                        "image": self.docker_image_url 
                    }
                ]
            }
        }
    
    def add_cloud_run_job(self, template, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return CloudRunJob(self.scope, self.coud_run_job_name, self.region, template=template, depends_on=depends_on)

    def build_http_target_trigger(self):
        return {
            'http_method': 'POST',
            'uri': f'https://{self.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/{self.project}/jobs/{self.coud_run_job_name}:run',
            'oauth_token': {
                'service_account_email': f'{self.service_account_email}'
            }
        }

    def add_cloud_scheduler_job(self, http_target, depends_on=None):
        depends_on = None if depends_on == [None] else depends_on
        return CloudSchedulerJob(
            self.scope, 
            self.cloud_scheduler_job_name, 
            self.scheduler_cron, 
            http_target=http_target,
            depends_on=depends_on
        )