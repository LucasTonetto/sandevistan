from constructs import Construct
from cdktf_cdktf_provider_google import cloudfunctions_function_iam_member

class CloudFunctionIamMember(cloudfunctions_function_iam_member.CloudfunctionsFunctionIamMember):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        cloud_function: str,
        member: str,
        role: str,
        **kwargs
    ):

        super().__init__(scope, id=id, cloud_function=cloud_function, member=member, role=role, **kwargs)