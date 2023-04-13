from constructs import Construct
from cdktf_cdktf_provider_google import project_iam_member

class ProjectIamMember(project_iam_member.ProjectIamMember):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        member: str,
        project: str,
        role: str,
        **kwargs
    ):

        super().__init__(scope, id, member=member, project=project, role=role, **kwargs)