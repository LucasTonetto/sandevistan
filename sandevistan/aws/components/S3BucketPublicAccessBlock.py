from constructs import Construct
from cdktf_cdktf_provider_aws import s3_bucket_public_access_block

class S3BucketPublicAccessBlock(s3_bucket_public_access_block.S3BucketPublicAccessBlock):

    def __init__(
        self, 
        scope: Construct, 
        bucket: str,
        block_public_access=True,
        **kwargs
    ):

        if(block_public_access == True):
            kwargs["block_public_acls"] = True
            kwargs["block_public_policy"] = True
            kwargs["ignore_public_acls"] = True
            kwargs["restrict_public_buckets"] = True

        s3_block_id = bucket + "-sandevistan-block-public-access"
        
        super().__init__(
            scope, 
            s3_block_id, 
            bucket=bucket, 
            **kwargs
        )