from constructs import Construct
from cdktf_cdktf_provider_google import pubsub_topic

class PubSubTopic(pubsub_topic.PubsubTopic):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        name: str,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        super().__init__(scope, id, name=name, **kwargs)