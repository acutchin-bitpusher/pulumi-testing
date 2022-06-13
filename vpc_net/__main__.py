import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
print( "   pulumi_stack_name: ", pulumi_stack_name )
print( " pulumi_project_name: ", pulumi_project_name )

resource_name_prefix = pulumi_project_name + "-" + pulumi_stack_name
print( "resource_name_prefix: ", resource_name_prefix )

env_config = config.require_object("env_config")

commontags = {
  "project": pulumi_project_name,
  "stack": pulumi_stack_name,
}

###  external ip address
#ip_addr = gcp.compute.Address.address(
#  resource_name = resource_name_prefix
#)
#external_ip = ip_addr.address

##  VPC/NETWORK
###  https://www.pulumi.com/registry/packages/gcp/api-docs/compute/network/
#network = gcp.compute.Network(
#  ## resource_name, positional first arg, Must be a match of regex '(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)',
#  resource_name_prefix,
#  name = resource_name_prefix,
#  description = env_config["vpc_net"]["description"],
#  routing_mode = env_config["vpc_net"]["routing_mode"],
#)
#pulumi.export( "vpc_net_gateway_ipv4", network.gateway_ipv4 )
#pulumi.export( "vpc_net_id", network.id )
###  "selfLInk" is supposed to be an output according to: https://www.pulumi.com/registry/packages/gcp/api-docs/compute/network/#id_python
##pulumi.export( "vpc_net_selfLink", network.selfLink )

#network = network.Vpc(
#  resource_name_prefix,
#  network.VpcArgs(
#    subnet_cidr_blocks = env_config["vpc_net"]["cidr_blocks"]
#  )
#)

#network_interface = [
#    {
#        'network': network.id,
#        'accessConfigs': [{'nat_ip': external_ip}],
#    }
#]

#firewall = gcp.compute.Firewall(
#  resource_name_prefix + "-" + "firewall",
#  network = network.self_link,
#  allows=[{
#    'protocol': "tcp",
#    'ports': ["22", "80", "443"]
#  }]
#)

#instance = compute.Instance('orb-pulumi-gcp', name='orb-pulumi-gcp', boot_disk=disk, machine_type='g1-small',
#                            network_interfaces=network_interface, metadata=meta_data)
#
## Export the DNS name of the bucket
#pulumi.export('instance_name', instance.name)
#pulumi.export('instance_meta_data', instance.metadata)
#pulumi.export('instance_network', instance.network_interfaces)
#pulumi.export('external_ip', addr.address)

