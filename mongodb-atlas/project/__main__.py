# -*- coding: utf-8 -*-
#This example illustrates how Provider objects can be used to create resources under
#different environmental configuration.
#https://www.pulumi.com/registry/packages/mongodbatlas/
#https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkpeering/
#https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/cluster/
#https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
#https://docs.atlas.mongodb.com/tutorial/manage-programmatic-access/
#https://docs.atlas.mongodb.com/tutorial/configure-api-access/project/create-one-api-key/

import pulumi
import pulumi_gcp as gcp
import pulumi_mongodbatlas as mongodbatlas
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

##  CLIENT/LOCAL VPC NETWORK PULUMI STACK REFERENCE
client_vpc_net_stack_ref = pulumi.StackReference( pulumi_org_name + "/" + env_config["client_vpc_net_pulumi_project_name"] + "/" + pulumi_stack_name )

##  MONGODB-ATLAS PROJECT
# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/project/
from project import Project, ProjectArgs
acbptest_mdba_project = Project(
    resource_name = pulumi_proj_stack,
    args=ProjectArgs(
        name = pulumi_proj_stack,
        org_id = mdba_org_id,
    ),
)
pulumi.export( "acbptest_mdba_project", acbptest_mdba_project )

##  MONGODB-ATLAS NETWORK CONTAINER
##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
##  https://www.mongodb.com/docs/atlas/reference/faq/networking/
##  https://www.mongodb.com/docs/atlas/reference/api/vpc-create-container/
from networkcontainer import NetworkContainer, NetworkContainerArgs
network_container = NetworkContainer(
    resource_name = pulumi_proj_stack,
    args=NetworkContainerArgs(
        atlas_cidr_block = env_config["mdba_network_container_cidr"],
        project_id = acbptest_mdba_project.project.id,
        provider_name = "GCP",
        ##  regions (optional): Provide this field only if you provide an atlas_cidr_block smaller than /18; https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
        #regions = [ env_config["mdba_network_container_gcp_region"] ],
    ),
)
pulumi.export( "mdba_network_container", network_container )

##  MONGODB-ATLAS NETWORK PEERING
##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkpeering/
##  https://www.mongodb.com/docs/atlas/security-vpc-peering/
from networkpeering import NetworkPeering, NetworkPeeringArgs, ResourceOptions
network_peering = NetworkPeering(
    resource_name = pulumi_proj_stack,
    opts = ResourceOptions(depends_on=[network_container]),
    args = NetworkPeeringArgs(
        ##  container_id (required): "Unique identifier of the MongoDB Atlas container for the provider (GCP). You can create an MongoDB Atlas container using the network_container resource or it can be obtained from the cluster returned values if a cluster has been created before the first container."
        container_id = network_container.net_container.container_id,
        ##  project_id (required): "The unique ID for the MongoDB Atlas project to create the database user"
        project_id = acbptest_mdba_project.project.id,
        ##  provider_name (required): "GCP|AWS|AZURE"
        provider_name = "GCP",
        ##  gcp_project_id: "GCP project ID of the owner of the network peer" (LOCAL SIDE)
        gcp_project_id = env_config["client_gcp_project_id"],
        ##  atlas_gcp_project_id: "The Atlas GCP Project ID for the GCP VPC used by your atlas cluster that it is need to set up the reciprocal connection" (ATLAS-SIDE/REMOTE)
        atlas_gcp_project_id = acbptest_mdba_project.id,
        ##  network_name (optional): "Name of the network peer to which Atlas connects."
        ##  NONE OF THE FOLLOWING WORK WITH THE NetworkPeering CLASS:
        #network_name = str( vpc_net["name"] ),
        #network_name = str( vpc_net["name"].apply( lambda x: x ) ),
        #network_name = str( vpc_net.apply( lambda x: x )["name"] ),
        #network_name = str( vpc_net_applied["name"] ),
        #network_name = str( client_vpc_net_name ),
        #network_name = str( client_vpc_net_name.apply( lambda x: x ) ),
        #network_name = str( client_vpc_net_stack_ref.get_output("vpc-net")["name"] ),
        #network_name = str( client_vpc_net_stack_ref.get_output( "vpc-net_name" ) ),
        #network_name = str( client_vpc_net_stack_ref.get_output( "vpc-net_name" ).apply( lambda x: x ) ),
        #network_name = str( pulumi.StackReference( pulumi_org_name + "/" + env_config["client_vpc_net_pulumi_project_name"] + "/" + pulumi_stack_name ).get_output( "client_vpc_net_name" ) )
        #network_name = str( pulumi.StackReference( pulumi_org_name + "/" + env_config["client_vpc_net_pulumi_project_name"] + "/" + pulumi_stack_name ).get_output( "client_vpc_net_name" ).apply( lambda x: x ) )
        ##  HERE WE USE A MANUALLY-ENTERED VALUE FROM THE ENV CONFIG FILE
        ##  BECAUSE WE CANNOT (FOR UNKOWN REASONS) PASS THE OUTPUT OF A STACKREFERENCE INTO THE OBJECT DEFINITION
        network_name = env_config["client_vpc_net_name"]
    ),
)
##  CREATING NETWORK PEERING OBJECT BASED ON THE MONGODB-ATLAS OBJECT DIRECTLY
##  ALLOWS USE OF STACKREFERENCE TO RETRIEVE THE CLIENT VPC NET NAME
#network_peering = mongodbatlas.NetworkPeering(
#    pulumi_proj_stack,
#    project_id = acbptest_mdba_project.project.id,
#    container_id = network_container.net_container.container_id,
#    provider_name="GCP",
#    gcp_project_id = env_config["client_gcp_project_id"],
#    network_name = client_vpc_net_stack_ref.get_output( "vpc-net_name" ),
#)
pulumi.export( "mdba_network_peering", network_peering )

##  CREATE GCP VPC NETWORK PEERING ACCEPTANCE?
##  BASED ON: https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkpeering/
#client_vpc_net_self_link = gcp.compute.get_network(
#    name = env_config["gcp_vpc_network"],
#    project = env_config["client_gcp_project_id"],
#).self_link    ##  BY READING GCP VPC NETWORK BY NAME & ID
client_vpc_net_self_link = client_vpc_net_stack_ref.get_output( "vpc-net_self_link" )    ##  FROM VPC-NET PULUMI STACK REFERENCE
gcp_peering = gcp.compute.NetworkPeering(
    pulumi_proj_stack,
    ##  network: "The primary network of the peering"
    network = client_vpc_net_self_link,
    ##  peer_network: "the peer network in the peering. The peer network may belong to a different project"
    ##  WHEN USING UV NetworkPeering CLASS FOR mdba_network_peering OBJECT
    peer_network = pulumi.Output.all( network_peering.networkpeering.atlas_gcp_project_id, network_peering.networkpeering.atlas_vpc_name).apply( lambda args: f"https://www.googleapis.com/compute/v1/projects/{args[0]}/global/networks/{args[1]}" )
    ##  WHEN USING mongodbatlas.NetworkPeering CLASS FOR mdba_network_peering OBJECT
    #peer_network = pulumi.Output.all( network_peering.atlas_gcp_project_id, network_peering.atlas_vpc_name).apply( lambda args: f"https://www.googleapis.com/compute/v1/projects/{args[0]}/global/networks/{args[1]}" )
)
pulumi.export( "gcp_peering", gcp_peering )

##  MONGODB-ATLAS IP ACCESS LIST
##  https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/projectipaccesslist/
acbptest_mdba_project_ip_access_list = mongodbatlas.ProjectIpAccessList(
    #"test",
    pulumi_proj_stack,
    #cidr_block = "1.2.3.4/32",
    cidr_block = env_config["client_vpc_net_cidr"],
    ##  comment (optional): APPEARS IN THE MDBA CONSOLE / PROJECT / NETWORK SETTINGS / IP ACCESS LISTS
    ##  NOTE: CANNOT BE CHANGED AFTER INITIAL CREATION, OR THE LIST WILL BE DELETED FROM MDBA AND THE RESOURCE WILL REMAIN IN THE PULUMI STACK!
    comment = env_config["client_vpc_net_name"],
    ##  "Unique identifier for the project to which you want to add one or more access list entries."; MDBA project id
    project_id = acbptest_mdba_project.project.id,
)
pulumi.export( "acbptest_mdba_project_ip_access_list", acbptest_mdba_project_ip_access_list )

