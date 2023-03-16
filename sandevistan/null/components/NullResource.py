from constructs import Construct
from cdktf_cdktf_provider_null import resource

class NullResource(resource.Resource):
    def __init__(
        self, 
        scope: Construct,
        **kwargs
    ):

        super().__init__(scope, **kwargs)