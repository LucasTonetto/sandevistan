from constructs import Construct
from cdktf_cdktf_provider_google import cloud_scheduler_job

class CloudSchedulerJob(cloud_scheduler_job.CloudSchedulerJob):
    def __init__(
        self, 
        scope: Construct,
        name: str,
        schedule: str,
        time_zone='America/Sao_Paulo',
        **kwargs
    ):

        super().__init__(scope, name, name=name, schedule=schedule, time_zone=time_zone, **kwargs)