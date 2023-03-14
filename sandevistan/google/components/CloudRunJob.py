from constructs import Construct
from cdktf_cdktf_provider_google import cloud_run_v2_job

class CloudRunJob(cloud_run_v2_job.CloudRunV2Job):
    def __init__(
        self, 
        scope: Construct,
        name: str,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        if("location" not in kwargs):
            kwargs["location"] = scope.region

        super().__init__(scope, name, name=name, launch_stage="BETA", **kwargs)