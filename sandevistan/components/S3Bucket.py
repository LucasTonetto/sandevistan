from constructs import Construct
from cdktf_cdktf_provider_aws import s3_bucket

class S3Bucket(s3_bucket.S3Bucket):

    def __init__(self, scope: Construct, bucket_id: str, **kwargs):

        if("tags" in kwargs):
            kwargs["tags"] = {"cdktf-sandevistan": scope.name, **kwargs["tags"]}
        else:
            kwargs["tags"] = {"cdktf-sandevistan": scope.name}

        if("lifecycle_rule" not in kwargs):
            kwargs["lifecycle_rule"] = [
                { "enabled": True, "id": "abort-multipart", "prefix": "/", "abortIncompleteMultipartUploadDays": 7 },
                { "enabled": True, "id": "standard-ia-files-30-days", "transition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                { "enabled": True, "id": "standard-ia-files-noncurrent-version-30-days", "noncurrentVersionTransition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                { "enabled": True, "id": "glacier-flexible-retrieval-files-180-days", "transition": [{ "days": 180, "storageClass": "GLACIER" }] },
                { "enabled": True, "id": "glacier-flexible-retrieval-files-noncurrent-version-180-days", "noncurrentVersionTransition": [{ "days": 180, "storageClass": "GLACIER" }] },
            ]

        super().__init__(scope, bucket_id, **kwargs)