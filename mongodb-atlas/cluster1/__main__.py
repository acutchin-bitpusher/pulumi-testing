# -*- coding: utf-8 -*-
#This example illustrates how Provider objects can be used to create resources under
#different environmental configuration.
#https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/cluster/
#https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
#https://docs.atlas.mongodb.com/tutorial/manage-programmatic-access/
#https://docs.atlas.mongodb.com/tutorial/configure-api-access/project/create-one-api-key/

import pulumi
import pulumi_mongodbatlas as mongodbatlas
import sys
sys.path.insert(0, '../../lib/mongodbatlas')

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
pulumi_proj_stack = pulumi_project_name + "-" + pulumi_stack_name
pulumi_org_name = config.require("pulumi_org_name")
mdba_org_id = config.require( "mdba_org_id" )
mdba_org_name = config.require( "mdba_org_name" )
env_config = config.require_object("env_config")

##  MONGODB-ATLAS PROJECT/NETWORK PULUMI STACK REFERENCE
mdba_project_stack_ref = pulumi.StackReference( pulumi_org_name + "/" + env_config["mdba_project_pulumi_project_name"] + "/" + pulumi_stack_name )
mdba_project_id = mdba_project_stack_ref.get_output("mdba_project")["project"]["id"]
pulumi.export( "mdba_project_id", mdba_project_id )

##  ATLAS/MONGODB CLUSTER/DATABASE
#from cluster import Cluster, ClusterArgs
#cluster = Cluster(
#    #resource_name = "my-custom-iac-mongo-cluster",
#    resource_name =  pulumi_proj_stack,
#    args = ClusterArgs(
#        #project_id = "610ab4f442d84c0b1b70e30e",
#        project_id = mdba_project_id,
#        #provider_instance_size_name = "M30",
#        provider_instance_size_name = env_config["mdba_instance_size_name"],
#        provider_name = "GCP",
#        backing_provider_name = None,
#        #auto_scaling_disk_gb_enabled = True,
#        auto_scaling_disk_gb_enabled = env_config["auto_scaling_disk_gb_enabled"],
#        # Optional
#        #name = "my-custom-mongo-cluster",
#        name = pulumi_proj_stack,
#        #cluster_type = "REPLICASET",
#        #cluster_type = env_config["cluster_type"], ## M0 CLUSTERS (FREE TIER) CANNOT SPEC CLUSTER TYPE
#        #provider_region_name = "CENTRAL_US",
#        provider_region_name = env_config["mdba_gcp_region_name"],
#        #mongo_db_major_version = "4.4",
#        mongo_db_major_version = env_config["mongo_db_major_version"],
#    ),
#)
cluster = mongodbatlas.Cluster(
    pulumi_proj_stack,
    project_id = mdba_project_id,
    provider_instance_size_name = env_config["mdba_instance_size_name"],
    provider_name = "GCP",
    auto_scaling_disk_gb_enabled = env_config["auto_scaling_disk_gb_enabled"],
    name = pulumi_proj_stack,
    provider_region_name = env_config["mdba_gcp_region_name"],
    ##  DOCUMENTATION DIFFERS AS TO WHAT IS ALLOWED HERE, SO GOING WITH DEFAULT FOR TESTING
    #mongo_db_major_version = env_config["mongo_db_major_version"],
)
pulumi.export( "cluster", cluster )

## https://docs.atlas.mongodb.com/reference/api/database-users/
## https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/databaseuser/
#from devops_plm_gcp_infra.mongodbatlas.alpha.dbuser import (
#    DbUser,
#    DbUserArgs,
#    mongodbatlas,
#)

#DbUser(
#    resource_name="my-custom-iac-mongo-user1",
#    args=DbUserArgs(
#        project_id="610ab4f442d84c0b1b70e30e",  # Change this value to match the desired Mongo DB Atlas Project ID
#        username="iacuser01",
#        roles=[
#            mongodbatlas.DatabaseUserRoleArgs(
#                database_name="my-custom-mongo-cluster", role_name="read"
#            )
#        ],  # DB Name is the cluster created in the previous step
#        auth_database_name="admin",
#        password="zxf7yd8fhsds78",  # This password has to be changed in the Mongo DB Console after creation
#        labels=[mongodbatlas.DatabaseUserLabelArgs(key="env", value="sandbox")],
#        scopes=[
#            mongodbatlas.DatabaseUserScopeArgs(
#                name="my-custom-mongo-cluster", type="CLUSTER"
#            )
#        ],  # DB Name is the cluster created in the previous step
#    ),
#)


# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/searchindex/
# https://docs.atlas.mongodb.com/reference/atlas-search/tutorial/create-index-ui/
# https://docs.atlas.mongodb.com/reference/api/fts-indexes-create-one/
# NOTICE: Keep in mind that in order to create an Index, there was a manually step to add sample data into the cluster created before so the DB gets created.

#from devops_plm_gcp_infra.mongodbatlas.alpha.searchindex import Index, IndexArgs

#Index(
#    resource_name="my-iac-index",
#    args=IndexArgs(
#        name="my-iac-index",
#        analyzer="lucene.standard",
#        cluster_name="my-custom-mongo-cluster",  # DB Name is the cluster created in the previous step
#        collection_name="pulumi",  # Change this to match your collection name
#        database="pulumitestdb",  # Change this to match your DB name
#        project_id="610ab4f442d84c0b1b70e30e",  # Change this value to match the desired Mongo DB Atlas Project ID
#        mappings_dynamic=True,
#    ),
#)


# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/searchindex/
# https://docs.atlas.mongodb.com/reference/atlas-search/tutorial/create-index-ui/

#from devops_plm_gcp_infra.mongodbatlas.alpha.teams import Team, TeamArgs

#Team(
#    resource_name="my-custom-iac-mongo-team1",
#    args=[
#        TeamArgs(
#            name="my-custom-iac-team",
#            org_id="61795f80e17d1a21780e34ee",  # Change this to match your Org ID in Mongo DB Atlas
#            usernames=[
#                "sample@email.com",
#            ],
#        ),
#    ],
#)

