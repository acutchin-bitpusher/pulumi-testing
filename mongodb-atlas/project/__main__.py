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

##  ATLAS/MONGODB PROJECT
##  CHANGE THIS TO A STACK REFERENCE?
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

##  ATLAS/MONGODB NETWORK CONTAINER
##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
##  https://docs.atlas.mongodb.com/reference/api/vpc-create-container/
##  https://docs.atlas.mongodb.com/security-vpc-peering/
from networkcontainer import NetworkContainer, NetworkContainerArgs
#atlas_network_container_cidr = config.require( "atlas_network_container_cidr" )
network_container = NetworkContainer(
  resource_name = pulumi_proj_stack,
  args=NetworkContainerArgs(
    atlas_cidr_block = env_config["mdba_network_container_cidr"],
    project_id = mdba_project.project.id,
    provider_name = "GCP",
    ##  Provide this field only if you provide an atlas_cidr_block smaller than /18
    ##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
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
    ##  container_id (required): MongoDB-Atlas network container id
    container_id = network_container.net_container.container_id,
    ##  project_id (required): The MongoDB-Atlas project id
    project_id = mdba_project.project.id,
    ##  provider_name (required): "GCP" or "AWS" ...
    provider_name = "GCP",
    ##  gcp_project_id: "GCP project ID of the owner of the network peer" (LOCAL SIDE)
    gcp_project_id = env_config["gcp_project_id"],
    ##  atlas_gcp_project_id: "the Atlas GCP Project ID for the GCP VPC used by your atlas cluster that it is need to set up the reciprocal connection" (ATLAS-SIDE/REMOTE)
    atlas_gcp_project_id = mdba_project.id,
    network_name = str( vpc_net["name"] ),
  ),
)
pulumi.export( "mdba_network_peering", network_peering )

###  CREATE GCP VPC NETWORK PEERING ACCEPTANCE?
###  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkpeering/
##gcp_vpc_network = gcp.compute.get_network(
##  name = env_config["gcp_vpc_network"],
##  project = env_config["gcp_project_id"],
##)
##pulumi.export( "gcp_vpc_network_self_link", gcp_vpc_network.self_link )
#vpc_net_self_link = vpc_net_stack_ref.get_output( "vpc-net_self_link" )
#pulumi.export( "vpc_net_self_link", vpc_net_self_link )
#gcp_peering = gcp.compute.NetworkPeering(
#  pulumi_proj_stack,
#  ##  network: "The primary network of the peering"
#  #network = gcp_vpc_network.self_link,
#  network = vpc_net_self_link,
#  ##  peer_network: "the peer network in the peering. The peer network may belong to a different project"
##  peer_network = pulumi.Output.all(
##    network_peering.networkpeering.atlas_gcp_project_id,
##    network_peering.networkpeering.atlas_vpc_name,
##  ).apply(lambda atlas_gcp_project_id, atlas_vpc_name: f"https://www.googleapis.com/compute/v1/projects/{atlas_gcp_project_id}/global/networks/{atlas_vpc_name}")
#  peer_network = 
#)
#pulumi.export( "gcp_peering", gcp_peering )
