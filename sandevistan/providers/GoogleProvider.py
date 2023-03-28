from constructs import Construct
from cdktf_cdktf_provider_google import provider

class GoogleProvider(provider.GoogleProvider):

    def __init__(
        self,
        scope: Construct,
        **kwargs
    ):

        if("region" not in kwargs):
            kwargs["region"] = scope.region

        super().__init__(
            scope,
            'google', 
            **kwargs
        )