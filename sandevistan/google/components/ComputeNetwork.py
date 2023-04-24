from constructs import Construct
from cdktf_cdktf_provider_google import compute_network

class ComputeNetwork(compute_network.ComputeNetwork):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        **kwargs
    ):

        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = id

        super().__init__(scope, id, name=name, **kwargs)