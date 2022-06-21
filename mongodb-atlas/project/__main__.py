# -*- coding: utf-8 -*-
#This example illustrates how Provider objects can be used to create resources under
#different environmental configuration.
#https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/cluster/
#https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
#https://docs.atlas.mongodb.com/tutorial/manage-programmatic-access/
#https://docs.atlas.mongodb.com/tutorial/configure-api-access/project/create-one-api-key/

import pulumi
import pulumi_gcp as gcp
import sys
sys.path.insert(0, '../../lib/mongodbatlas')

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
pulumi_org_name = config.require("pulumi_org_name")
mdba_org_id = config.require( "mdba_org_id" )
mdba_org_name = config.require( "mdba_org_name" )
pulumi_proj_stack = pulumi_project_name + "-" + pulumi_stack_name
env_config = config.require_object("env_config")

##  MONGODB-ATLAS PROJECT
# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/project/
from project import Project, ProjectArgs
mdba_project = Project(
  resource_name = pulumi_proj_stack,
  args=ProjectArgs(
    name = pulumi_proj_stack,
    org_id = mdba_org_id,
  ),
)
pulumi.export( "mdba_project", mdba_project )

##  MONGODB-ATLAS NETWORK CONTAINER
##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
##  https://docs.atlas.mongodb.com/reference/api/vpc-create-container/
##  https://docs.atlas.mongodb.com/security-vpc-peering/
from networkcontainer import NetworkContainer, NetworkContainerArgs
network_container = NetworkContainer(
  resource_name = pulumi_proj_stack,
  args=NetworkContainerArgs(
    atlas_cidr_block = env_config["mdba_network_container_cidr"],
    project_id = mdba_project.project.id,
    provider_name = "GCP",
    ##  regions (optional): Provide this field only if you provide an atlas_cidr_block smaller than /18; https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
    #regions = [ env_config["mdba_network_container_gcp_region"] ],
  ),
)
pulumi.export( "mdba_network_container", network_container )

##  MONGODB-ATLAS NETWORK PEERING
##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkpeering/
vpc_net_stack_ref = pulumi.StackReference( pulumi_org_name + "/" + env_config["vpc_net_pulumi_project_name"] + "/" + pulumi_stack_name )
vpc_net = vpc_net_stack_ref.get_output( "vpc-net" )
pulumi.export( "vpc_net_name", vpc_net["name"] )
from networkpeering import NetworkPeering, NetworkPeeringArgs, ResourceOptions
network_peering = NetworkPeering(
  resource_name = pulumi_proj_stack,
  opts=ResourceOptions(depends_on=[network_container]),
  args=NetworkPeeringArgs(
    ##  container_id (required): "Unique identifier of the MongoDB Atlas container for the provider (GCP). You can create an MongoDB Atlas container using the network_container resource or it can be obtained from the cluster returned values if a cluster has been created before the first container."
    container_id = network_container.net_container.container_id,
    ##  project_id (required): "The unique ID for the MongoDB Atlas project to create the database user"
    project_id = mdba_project.project.id,
    ##  provider_name (required): "GCP|AWS|AZURE"
    provider_name = "GCP",
    ##  gcp_project_id: "GCP project ID of the owner of the network peer" (LOCAL SIDE)
    gcp_project_id = env_config["gcp_project_id"],
    ##  atlas_gcp_project_id: "The Atlas GCP Project ID for the GCP VPC used by your atlas cluster that it is need to set up the reciprocal connection" (ATLAS-SIDE/REMOTE)
    atlas_gcp_project_id = mdba_project.id,
    ##  network_name (optional): "Name of the network peer to which Atlas connects."
    network_name = str( vpc_net["name"] ),
  ),
)
pulumi.export( "mdba_network_peering", network_peering )

##  CREATE GCP VPC NETWORK PEERING ACCEPTANCE?
##  BASED ON: https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkpeering/
##  GET GCP VPC NETWORK SELF LINK:
#vpc_net_self_link = gcp.compute.get_network(
#  name = env_config["gcp_vpc_network"],
#  project = env_config["gcp_project_id"],
#).self_link  ##  BY READING GCP VPC NETWORK BY NAME & ID
vpc_net_self_link = vpc_net_stack_ref.get_output( "vpc-net_self_link" )  ##  FROM VPC-NET PULUMI STACK REFERENCE
gcp_peering = gcp.compute.NetworkPeering(
  pulumi_proj_stack,
  ##  network: "The primary network of the peering"
  network = vpc_net_self_link,
  ##  peer_network: "the peer network in the peering. The peer network may belong to a different project"
  peer_network = pulumi.Output.all( network_peering.networkpeering.atlas_gcp_project_id, network_peering.networkpeering.atlas_vpc_name).apply( lambda args: f"https://www.googleapis.com/compute/v1/projects/{args[0]}/global/networks/{args[1]}" )
)
pulumi.export( "gcp_peering", gcp_peering )
