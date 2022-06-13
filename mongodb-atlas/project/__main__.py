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
Project(
    #resource_name = "my-custom-iac-mongo-project",
    resource_name = pulumi_proj_stack,
    args=ProjectArgs(
        #name = "my-custom-iac-mongo-project",
        name = pulumi_proj_stack,
        #org_id="61795f80e17d1a21780e34ee",  # Change this to match your Org ID in Mongo DB Atlas
        org_id = mdba_org_id,
    ),
)

#pulumi.export('instance_name', ssh_instance.name)
#pulumi.export('instance_meta_data', ssh_instance.metadata)
#pulumi.export('instance_network', ssh_instance.network_interfaces)
