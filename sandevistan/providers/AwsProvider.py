from constructs import Construct
from cdktf_cdktf_provider_aws import provider

class AwsProvider(provider.AwsProvider):

    def __init__(
        self,
        scope: Construct,
        **kwargs
    ):
        super().__init__(
            scope,
            'aws', 
            **kwargs
        )