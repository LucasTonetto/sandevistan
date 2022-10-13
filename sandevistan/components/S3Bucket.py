from constructs import Construct
from cdktf_cdktf_provider_aws import s3_bucket

class S3Bucket(s3_bucket.S3Bucket):

    def __init__(self, scope: Construct, bucket_id: str, **kwargs):

        tags = {"cdktf-sandevistan": scope.name}

        if("tags" in kwargs):
            tags = {**tags, **kwargs["tags"]}
            del kwargs["tags"]

        super().__init__(scope, bucket_id, tags=tags, **kwargs)