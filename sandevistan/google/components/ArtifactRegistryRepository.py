from constructs import Construct
from cdktf_cdktf_provider_google import artifact_registry_repository

class ArtifactRegistryRepository(artifact_registry_repository.ArtifactRegistryRepository):
    def __init__(
        self, 
        scope: Construct,
        name: str,
        location: str,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        super().__init__(scope, name, location=location, repository_id=name, **kwargs)