import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
pulumi_proj_stack = pulumi_project_name + "-" + pulumi_stack_name
env_config = config.require_object("env_config")

##  EXTERNAL IP ADDRESS
ip_addr = gcp.compute.Address(
  resource_name = pulumi_proj_stack
)
external_ip = ip_addr.address
pulumi.export('external_ip', ip_addr.address)

##  VPC/NETWORK
##  https://www.pulumi.com/registry/packages/gcp/api-docs/compute/network/
network = gcp.compute.Network(
  ## resource_name; positional first arg; must match regex: '(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)'
  pulumi_proj_stack,
  name = pulumi_proj_stack,
  description = env_config["description"],
  routing_mode = env_config["routing_mode"],
)
pulumi.export( "vpc-net",               network )
pulumi.export( "vpc-net_gateway_ipv4",  network.gateway_ipv4.apply(lambda x: x) )
pulumi.export( "vpc-net_id",            network.id.apply(lambda x: x) )
pulumi.export( "vpc-net_self_link",     network.self_link.apply(lambda x: x) )
pulumi.export( "vpc-net_name",          network.name.apply(lambda x: x) )
