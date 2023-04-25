from constructs import Construct
from sandevistan.google.components.ComputeInstance import ComputeInstance
from sandevistan.google.components.ComputeNetwork import ComputeNetwork
from sandevistan.google.components.ComputeFirewall import ComputeFirewall
from sandevistan.google.components.ComputeAddress import ComputeAddress
from sandevistan.providers.GoogleProvider import GoogleProvider

class ComputeInstanceWithFirewall():
    def __init__(
        self,
        scope: Construct, 
        stack_name: str,
        project: str,
        location: str,
        zone: str,
        service_account_key_path: str,
        network_name: str,
        firewall_source_ranges: list,
        compute_firewall_allow: list = None
    ):

        self.scope = scope
        self.stack_name = stack_name
        self.project = project
        self.location = location
        self.zone = zone
        self.service_account_key_path = service_account_key_path
        self.network_name = network_name
        self.firewall_source_ranges = firewall_source_ranges
        self.compute_firewall_allow = compute_firewall_allow

        self.add_gcp_provider()

        ip = self.add_compute_address()

        vpc = self.add_compute_network()

        firewall = self.add_compute_firewall(vpc)

        self.add_compute_instance(ip, firewall)

    def add_gcp_provider(self):
        return GoogleProvider(
            self.scope,
            credentials=self.service_account_key_path,
            project=self.project,
            region=self.location
        )
    
    def add_compute_address(self):
        return ComputeAddress(
            self.scope,
            self.stack_name + '-compute-address',
            region=self.location
        )
        
    def add_compute_network(self):
        return ComputeNetwork(
            self.scope,
            self.network_name
        )
    
    def add_compute_firewall(self, vpc):
        allow = self.compute_firewall_allow \
            if self.compute_firewall_allow is not None \
            else [{'protocol': 'tcp', 'ports': ['80', '8080', '22']}]
        return ComputeFirewall(
            self.scope,
            self.stack_name + '-compute-firewall',
            network=self.network_name,
            allow=allow,
            source_ranges=self.firewall_source_ranges,
            depends_on=[vpc]
        )
    
    def add_compute_instance(self, ip, firewall):
        return ComputeInstance(
            self.scope,
            self.stack_name + '-compute-instance',
            zone=self.zone,
            network_interface=[
                {
                    'network': self.network_name,
                    'accessConfig': [
                        {
                            'natIp': ip.address
                        }
                    ]
                },
            ],
            tags=['http-server', 'https-server'],
            depends_on=[firewall, ip]
        )