from constructs import Construct
from cdktf_cdktf_provider_google import cloudfunctions_function

class CloudFunction(cloudfunctions_function.CloudfunctionsFunction):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        name: str,
        runtime: str,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        
        super().__init__(scope, id, name=name, runtime=runtime, **kwargs)