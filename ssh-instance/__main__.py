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

vpc_net_stack_ref = pulumi.StackReference( f"{pulumi_org_name}/acbptest-network/{pulumi_stack_name}" )
pulumi.export( "vpc_network_self_link", vpc_net_stack_ref.get_output("vpc_net_self_link") )

##  CAN'T PRINT AN OUTPUT (EVEN FROM ANOTHER STACK)
##  BECAUSE AN OUTPUT IS A CONTAINER FOR A DEFERRED VALUE THAT IS NOT YET AVAILABLE WHEN PRINT IS CALLED
##  PRINTS SOMETHING LIKE: "<pulumi.output.Output object at 0x106c3e2e0>"
#print( "vpc_network_self_link: ", vpc_net_stack_ref.get_output("vpc_net_self_link") )

vpc_network = vpc_net_stack_ref.get_output( "vpc_network" )
pulumi.export( "vpc_network_name", vpc_network["name"] )

firewall = gcp.compute.Firewall(
  resource_name_prefix,
  #project = pulumi_project_name,
  network = vpc_net_stack_ref.get_output("vpc_net_self_link"),
  source_tags = ["ssh-ingress"],
  allows = [
    gcp.compute.FirewallAllowArgs(
      protocol="icmp"
    ),
    gcp.compute.FirewallAllowArgs(
      protocol="tcp",
      ports=["22", "80", "443"],
    ),
  ],
)

#default_account = gcp.service_account.Account(
#  "defaultAccount",
#  #resource_name_prefix + "-" + "ssh-instance",
#  account_id="service_account_id",
#  display_name="Service Account"
#  #display_name = ( resource_name_prefix + "-" + "ssh-instance" ),
#)
ssh_instance = gcp.compute.Instance(
  resource_name_prefix,
  name = resource_name_prefix,
  machine_type = "f1-micro",
  zone = ( env_config["gcp_region"] + "-a" ),
  tags = [
    "ssh-ingress",
  ],
  boot_disk=gcp.compute.InstanceBootDiskArgs(
    initialize_params=gcp.compute.InstanceBootDiskInitializeParamsArgs(
      image="debian-cloud/debian-9",
    ),
  ),
#  scratch_disks=[gcp.compute.InstanceScratchDiskArgs(
#    interface="SCSI",
#  )],
  network_interfaces=[
    gcp.compute.InstanceNetworkInterfaceArgs(
      #network="default",
      network = vpc_net_stack_ref.get_output("vpc_net_self_link"),
      access_configs = [
        gcp.compute.InstanceNetworkInterfaceAccessConfigArgs()
      ],
    )
  ],
  metadata={
    "foo": "bar",
  },
  metadata_startup_script="echo hi > /test.txt",
#  service_account = gcp.compute.InstanceServiceAccountArgs(
#    email = default_account.email,
#    scopes = ["cloud-platform"],
#  )
)
pulumi.export('instance_name', ssh_instance.name)
pulumi.export('instance_meta_data', ssh_instance.metadata)
pulumi.export('instance_network', ssh_instance.network_interfaces)