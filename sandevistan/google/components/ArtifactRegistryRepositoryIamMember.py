from constructs import Construct
from cdktf_cdktf_provider_google import artifact_registry_repository_iam_member

class ArtifactRegistryRepositoryIamMember(artifact_registry_repository_iam_member.ArtifactRegistryRepositoryIamMember):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        member: str,
        repository: str,
        role: str, 
        **kwargs
    ):

        super().__init__(scope, id_=id, member=member, repository=repository, role=role, **kwargs)