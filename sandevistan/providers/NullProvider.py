from constructs import Construct
from cdktf_cdktf_provider_null import provider as null_provider

class NullProvider(null_provider.NullProvider):
    def __init__(
        self, 
        scope: Construct,
        **kwargs
    ):

        super().__init__(scope, **kwargs)