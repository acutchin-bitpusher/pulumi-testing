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

##  EXTERNAL IP ADDRESS
ip_addr = gcp.compute.Address(
  resource_name = resource_name_prefix
)
external_ip = ip_addr.address
pulumi.export('external_ip', ip_addr.address)

##  VPC/NETWORK
##  https://www.pulumi.com/registry/packages/gcp/api-docs/compute/network/
network = gcp.compute.Network(
  ## resource_name; positional first arg; must match regex: '(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)',
  resource_name_prefix,
  name = resource_name_prefix,
  description = env_config["vpc_net"]["description"],
  routing_mode = env_config["vpc_net"]["routing_mode"],
)
pulumi.export( "vpc_net_gateway_ipv4", network.gateway_ipv4 )
pulumi.export( "vpc_net_id", network.id )
##  "selfLInk" is supposed to be an output according to: https://www.pulumi.com/registry/packages/gcp/api-docs/compute/network/#id_python
pulumi.export( "vpc_net_self_link", network.self_link )
pulumi.export( "vpc_network", network )


