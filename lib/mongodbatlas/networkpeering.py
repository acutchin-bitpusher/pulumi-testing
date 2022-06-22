# -*- coding: utf-8 -*-

from typing import Any, Optional

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["NetworkPeeringArgs", "NetworkPeering"]


class NetworkPeeringArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas Network Container VPC` resource.
    """

    # required
    container_id: Any
    project_id: Any
    provider_name: str

    # optional
    atlas_gcp_project_id: Optional[str] = None
    gcp_project_id: Optional[str] = None
    network_name: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class NetworkPeering(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: NetworkPeeringArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongo/alpha:MongoNetworkPeering",
            name=f"{resource_name}-mongonetworkpeering",
            props={},
            opts=opts,
        )
        ###############################################################################
        self_parent = self
        child_opts = ResourceOptions(parent=self_parent)
        ###############################################################################
        # SetResources
        ###############################################################################
        try:
            self.networkpeering = mongodbatlas.NetworkPeering(
                resource_name=resource_name,
                container_id=args.container_id,
                project_id=args.project_id,
                provider_name=args.provider_name,
                gcp_project_id=args.gcp_project_id, ##  GCP project ID of the owner of the network peer (LOCAL SIDE)
                atlas_gcp_project_id=args.atlas_gcp_project_id, ## The Atlas GCP Project ID for the GCP VPC used by your atlas cluster that it is need to set up the reciprocal connection. (ATLAS-SIDE/REMOTE)
                network_name=args.network_name,
                opts=child_opts,
            )
        except Exception as ex:
            log.error(f"MongoNetworkPeering -> {ex.args[0]}")
        ###############################################################################
