from constructs import Construct
from sandevistan.aws.components.S3Bucket import S3Bucket
from sandevistan.errors.MissingArguments import MissingArguments

class DataLake():

    def __init__(
        self, 
        scope: Construct, 
        bucket_names: str,
        block_public_access=True,
        sufix_of_layers=['raw', 'curated', 'processed'],
        **kwargs
    ):

        if("lifecycle_rule" not in kwargs):
            kwargs["lifecycle_rule"] = [
                [
                    { "enabled": True, "id": "abort-multipart", "prefix": "/", "abortIncompleteMultipartUploadDays": 7 },
                    { "enabled": True, "id": "standard-ia-files-30-days", "transition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                    { "enabled": True, "id": "standard-ia-files-noncurrent-version-30-days", "noncurrentVersionTransition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                    { "enabled": True, "id": "glacier-flexible-retrieval-files-60-days", "transition": [{ "days": 60, "storageClass": "GLACIER" }] },
                    { "enabled": True, "id": "glacier-flexible-retrieval-files-noncurrent-version-60-days", "noncurrentVersionTransition": [{ "days": 60, "storageClass": "GLACIER" }] },
                ],
                [
                    { "enabled": True, "id": "abort-multipart", "prefix": "/", "abortIncompleteMultipartUploadDays": 7 },
                    { "enabled": True, "id": "standard-ia-files-30-days", "transition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                    { "enabled": True, "id": "standard-ia-files-noncurrent-version-30-days", "noncurrentVersionTransition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                    { "enabled": True, "id": "glacier-flexible-retrieval-files-90-days", "transition": [{ "days": 90, "storageClass": "GLACIER" }] },
                    { "enabled": True, "id": "glacier-flexible-retrieval-files-noncurrent-version-90-days", "noncurrentVersionTransition": [{ "days": 90, "storageClass": "GLACIER" }] },
                ],
                [
                    { "enabled": True, "id": "abort-multipart", "prefix": "/", "abortIncompleteMultipartUploadDays": 7 },
                    { "enabled": True, "id": "standard-ia-files-30-days", "transition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                    { "enabled": True, "id": "standard-ia-files-noncurrent-version-30-days", "noncurrentVersionTransition": [{ "days": 30, "storageClass": "STANDARD_IA" }] },
                    { "enabled": True, "id": "glacier-flexible-retrieval-files-180-days", "transition": [{ "days": 180, "storageClass": "GLACIER" }] },
                    { "enabled": True, "id": "glacier-flexible-retrieval-files-noncurrent-version-180-days", "noncurrentVersionTransition": [{ "days": 180, "storageClass": "GLACIER" }] },
                ]
            ]

        for index, layer in enumerate(sufix_of_layers):
            args = {}
            number_of_layers = len(sufix_of_layers)
            for elm in kwargs:
                if number_of_layers != len(kwargs[elm]):
                    raise MissingArguments(number_of_layers, len(kwargs[elm]))
                args[elm] = kwargs[elm][index]
            bucket =  bucket_names + '-' + layer
            S3Bucket(scope, bucket, block_public_access, **args)