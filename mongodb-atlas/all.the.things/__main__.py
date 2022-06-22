# -*- coding: utf-8 -*-
"""
This example illustrates how Provider objects can be used to create resources under
different environmental configuration.
https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/cluster/
https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
https://docs.atlas.mongodb.com/tutorial/manage-programmatic-access/
https://docs.atlas.mongodb.com/tutorial/configure-api-access/project/create-one-api-key/
"""
from devops_plm_gcp_infra.mongodbatlas.alpha.cluster import Cluster, ClusterArgs

cluster1 = Cluster(
    resource_name="my-custom-iac-mongo-cluster",
    args=ClusterArgs(
        # Required
        project_id="610ab4f442d84c0b1b70e30e",  # Change this value to match the desired Mongo DB Atlas Project ID
        provider_instance_size_name="M30",
        provider_name="GCP",
        backing_provider_name=None,
        auto_scaling_disk_gb_enabled=True,
        # Optional
        name="my-custom-mongo-cluster",
        cluster_type="REPLICASET",
        provider_region_name="CENTRAL_US",
        mongo_db_major_version="4.4",
    ),
)


# https://docs.atlas.mongodb.com/reference/api/database-users/
# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/databaseuser/
from devops_plm_gcp_infra.mongodbatlas.alpha.dbuser import (
    DbUser,
    DbUserArgs,
    mongodbatlas,
)

DbUser(
    resource_name="my-custom-iac-mongo-user1",
    args=DbUserArgs(
        project_id="610ab4f442d84c0b1b70e30e",  # Change this value to match the desired Mongo DB Atlas Project ID
        username="iacuser01",
        roles=[
            mongodbatlas.DatabaseUserRoleArgs(
                database_name="my-custom-mongo-cluster", role_name="read"
            )
        ],  # DB Name is the cluster created in the previous step
        auth_database_name="admin",
        password="zxf7yd8fhsds78",  # This password has to be changed in the Mongo DB Console after creation
        labels=[mongodbatlas.DatabaseUserLabelArgs(key="env", value="sandbox")],
        scopes=[
            mongodbatlas.DatabaseUserScopeArgs(
                name="my-custom-mongo-cluster", type="CLUSTER"
            )
        ],  # DB Name is the cluster created in the previous step
    ),
)


# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/searchindex/
# https://docs.atlas.mongodb.com/reference/atlas-search/tutorial/create-index-ui/
# https://docs.atlas.mongodb.com/reference/api/fts-indexes-create-one/
# NOTICE: Keep in mind that in order to create an Index, there was a manually step to add sample data into the cluster created before so the DB gets created.

from devops_plm_gcp_infra.mongodbatlas.alpha.searchindex import Index, IndexArgs

Index(
    resource_name="my-iac-index",
    args=IndexArgs(
        name="my-iac-index",
        analyzer="lucene.standard",
        cluster_name="my-custom-mongo-cluster",  # DB Name is the cluster created in the previous step
        collection_name="pulumi",  # Change this to match your collection name
        database="pulumitestdb",  # Change this to match your DB name
        project_id="610ab4f442d84c0b1b70e30e",  # Change this value to match the desired Mongo DB Atlas Project ID
        mappings_dynamic=True,
    ),
)


# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/searchindex/
# https://docs.atlas.mongodb.com/reference/atlas-search/tutorial/create-index-ui/

from devops_plm_gcp_infra.mongodbatlas.alpha.teams import Team, TeamArgs

Team(
    resource_name="my-custom-iac-mongo-team1",
    args=[
        TeamArgs(
            name="my-custom-iac-team",
            org_id="61795f80e17d1a21780e34ee",  # Change this to match your Org ID in Mongo DB Atlas
            usernames=[
                "sample@email.com",
            ],
        ),
    ],
)


# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/project/

from devops_plm_gcp_infra.mongodbatlas.alpha.project import Project, ProjectArgs

Project(
    resource_name="my-custom-iac-mongo-project",
    args=ProjectArgs(
        name="my-custom-iac-mongo-project",
        org_id="61795f80e17d1a21780e34ee",  # Change this to match your Org ID in Mongo DB Atlas
    ),
)


# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
# https://docs.atlas.mongodb.com/reference/api/vpc-create-container/
# https://docs.atlas.mongodb.com/security-vpc-peering/


from devops_plm_gcp_infra.mongodbatlas.alpha.networkcontainer import (
    NetworkContainer,
    NetworkContainerArgs,
)

container1 = NetworkContainer(
    resource_name="my-custom-iac-mongo-vpc",
    args=NetworkContainerArgs(
        atlas_cidr_block="10.8.0.0/21",
        project_id="61b756e95956bc73c48944fe",  # Change this value to match the desired Mongo DB Atlas Project ID
        provider_name="GCP",
        regions=["CENTRAL_US"],
    ),
)

# https://www.pulumi.com/registry/packages/mongodbatlas/api-docs/networkcontainer/
# https://docs.atlas.mongodb.com/reference/api/vpc-create-container/
# https://docs.atlas.mongodb.com/security-vpc-peering/
# https://docs.mongodb.com/mongocli/v1.16/reference/atlas/networking-containers-list/

from devops_plm_gcp_infra.mongodbatlas.alpha.networkpeering import (
    NetworkPeering,
    NetworkPeeringArgs,
    ResourceOptions,
)

NetworkPeering(
    resource_name="my-custom-iac-mongo-vpc-peering",
    opts=ResourceOptions(depends_on=[container1]),
    args=NetworkPeeringArgs(
        container_id="61b76758776cd47e697667be",  # See this in order to obtain container id value from previous step https://docs.mongodb.com/mongocli/v1.16/reference/atlas/networking-containers-list/
        project_id="61b756e95956bc73c48944fe",  # Change this value to match the desired Mongo DB Atlas Project ID
        provider_name="GCP",
        gcp_project_id="univision-test-ott-apps",
        atlas_gcp_project_id="univision-test-ott-apps",
        network_name="default",
    ),
)
