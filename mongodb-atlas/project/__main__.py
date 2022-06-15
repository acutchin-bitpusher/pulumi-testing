# -*- coding: utf-8 -*-
#This example illustrates how Provider objects can be used to create resources under
#different environmental configuration.
#https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/cluster/
#https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
#https://docs.atlas.mongodb.com/tutorial/manage-programmatic-access/
#https://docs.atlas.mongodb.com/tutorial/configure-api-access/project/create-one-api-key/

import pulumi

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
pulumi_org_name = config.require("pulumi_org_name")
print( "   pulumi_stack_name: ", pulumi_stack_name )
print( " pulumi_project_name: ", pulumi_project_name )

mdba_org_id = config.require( "mdba_org_id" )
print( "mdba_org_id: ", mdba_org_id )

mdba_org_name = config.require( "mdba_org_name" )
print( "mdba_org_name: ", mdba_org_name )

pulumi_proj_stack = pulumi_project_name + "-" + pulumi_stack_name
print( "pulumi_proj_stack: ", pulumi_proj_stack )

env_config = config.require_object("env_config")

##  ATLAS/MONGODB PROJECT
# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/project/
import sys
sys.path.insert(0, '../../lib/mongodbatlas')
from project import Project, ProjectArgs
mdba_project = Project(
    #resource_name = "my-custom-iac-mongo-project",
    resource_name = pulumi_proj_stack,
    args=ProjectArgs(
        #name = "my-custom-iac-mongo-project",
        name = pulumi_proj_stack,
        #org_id="61795f80e17d1a21780e34ee",  # Change this to match your Org ID in Mongo DB Atlas
        org_id = mdba_org_id,
    ),
)
pulumi.export( "mdba_project", mdba_project )

##  ATLAS/MONGODB PROJECT NETWORK CONTAINER
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

## https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
## https://docs.atlas.mongodb.com/reference/api/vpc-create-container/
## https://docs.atlas.mongodb.com/security-vpc-peering/
## https://docs.mongodb.com/mongocli/v1.16/reference/atlas/networking-containers-list/
#
#from devops_plm_gcp_infra.mongodbatlas.alpha.networkpeering import (
#    NetworkPeering,
#    NetworkPeeringArgs,
#    ResourceOptions,
#)
#
#NetworkPeering(
#    resource_name="my-custom-iac-mongo-vpc-peering",
#    opts=ResourceOptions(depends_on=[container1]),
#    args=NetworkPeeringArgs(
#        container_id="61b76758776cd47e697667be",  # See this in order to obtain container id value from previous step https://docs.mongodb.com/mongocli/v1.16/reference/atlas/networking-containers-list/
#        project_id="61b756e95956bc73c48944fe",  # Change this value to match the desired Mongo DB Atlas Project ID
#        provider_name="GCP",
#        gcp_project_id="univision-test-ott-apps",
#        atlas_gcp_project_id="univision-test-ott-apps",
#        network_name="default",
#    ),
#)
