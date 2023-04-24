from constructs import Construct
from cdktf_cdktf_provider_google import compute_instance

class ComputeInstance(compute_instance.ComputeInstance):
    def __init__(
        self, 
        scope: Construct,
        id: str,
        boot_disk: dict = None,
        machine_type: str = 'e2-medium',
        network_interface: dict = None,
        zone: str = None,
        **kwargs
    ):

        if boot_disk is None:
            boot_disk = {
                'initialize_params': {
                    'image': 'debian-cloud/debian-11',
                    'labels': {
                        'cdktf-sandevistan': scope.name
                    }
                }
            }
        else:
            if 'labels' in boot_disk['initialize_params']:
                new_labels = {'cdktf-sandevistan': scope.name, **boot_disk['initialize_params']['labels']}
                boot_disk['initialize_params']['labels'] = new_labels
            else:
                boot_disk['initialize_params']['labels'] = {'cdktf-sandevistan': scope.name}

        if network_interface is None:
            network_interface = [
                {
                    'network': 'default'
                }
            ]

        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = id

        super().__init__(scope, id, name=name, machine_type=machine_type, boot_disk=boot_disk, network_interface=network_interface, zone=zone, **kwargs)