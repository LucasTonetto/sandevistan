from constructs import Construct
from cdktf_cdktf_provider_google import secret_manager_secret_version

class SecretManagerSecretVersion(secret_manager_secret_version.SecretManagerSecretVersion):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        secret: str,
        secret_data: str,
        **kwargs
    ):

        super().__init__(scope, id, secret=secret, secret_data=secret_data, **kwargs)