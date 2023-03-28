from constructs import Construct
from cdktf_cdktf_provider_google import storage_bucket_object

class StorageBucketObject(storage_bucket_object.StorageBucketObject):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        bucket: str,
        name: str,
        **kwargs
    ):

        super().__init__(scope, id, bucket=bucket, name=name, **kwargs)