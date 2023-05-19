from constructs import Construct
from cdktf_cdktf_provider_google import sourcerepo_repository

class SourcerepoRepository(sourcerepo_repository.SourcerepoRepository):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        **kwargs
    ):

        super().__init__(scope, id, name=id, **kwargs)