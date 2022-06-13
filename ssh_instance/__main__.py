import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
pulumi_org_name = config.require("org")
print( "   pulumi_stack_name: ", pulumi_stack_name )
print( " pulumi_project_name: ", pulumi_project_name )

resource_name_prefix = pulumi_project_name + "-" + pulumi_stack_name
print( "resource_name_prefix: ", resource_name_prefix )

env_config = config.require_object("env_config")

commontags = {
  "project": pulumi_project_name,
  "stack": pulumi_stack_name,
}

stack_ref = pulumi.StackReference(f"{org}/my-first-app/{stack}")

pulumi.export("shopUrl", stack_ref.get_output("url"))


#firewall = gcp.compute.Firewall(
#  resource_name_prefix + "-" + "ssh-instance",
#  network = network.self_link,
#  allows=[{
#    'protocol': "tcp",
#    'ports': ["22", "80", "443"]
#  }]
#  source_tags = ["some_mysterious_tag"]
#)
#
#network_interface = [
#    {
#        'network': network.id,
#        'accessConfigs': [{'nat_ip': external_ip}],
#    }
#]
#
#instance = compute.Instance('orb-pulumi-gcp', name='orb-pulumi-gcp', boot_disk=disk, machine_type='g1-small',
#                            network_interfaces=network_interface, metadata=meta_data)
#
## Export the DNS name of the bucket
#pulumi.export('instance_name', instance.name)
#pulumi.export('instance_meta_data', instance.metadata)
#pulumi.export('instance_network', instance.network_interfaces)
#
