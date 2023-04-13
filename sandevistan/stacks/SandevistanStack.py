from cdktf import TerraformStack
from constructs import Construct
import sys

class SandevistanStack(TerraformStack):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        self.name = name

        sys.path.insert(0,'../..')