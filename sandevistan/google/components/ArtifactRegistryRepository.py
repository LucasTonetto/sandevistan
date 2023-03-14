from constructs import Construct
from cdktf_cdktf_provider_google import artifact_registry_repository

class ArtifactRegistryRepository(artifact_registry_repository.ArtifactRegistryRepository):
    def __init__(
        self, 
        scope: Construct,
        name: str,
        format='DOCKER',
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        if("location" not in kwargs):
            kwargs["location"] = scope.region

        super().__init__(scope, name, format=format, repository_id=name, **kwargs)