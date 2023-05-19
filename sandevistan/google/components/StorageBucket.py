from constructs import Construct
from cdktf_cdktf_provider_google import storage_bucket

class StorageBucket(storage_bucket.StorageBucket):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        location: str,
        name: str,
        force_destroy: bool = False,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        super().__init__(scope, id, location=location, name=name, force_destroy=force_destroy, **kwargs)