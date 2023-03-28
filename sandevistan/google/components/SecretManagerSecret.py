from constructs import Construct
from cdktf_cdktf_provider_google import secret_manager_secret

class SecretManagerSecret(secret_manager_secret.SecretManagerSecret):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        secret_id: str,
        replication,
        **kwargs
    ):

        if("labels" in kwargs):
            kwargs["labels"] = {"cdktf-sandevistan": scope.name, **kwargs["labels"]}
        else:
            kwargs["labels"] = {"cdktf-sandevistan": scope.name}

        super().__init__(scope, id, secret_id=secret_id, replication=replication, **kwargs)