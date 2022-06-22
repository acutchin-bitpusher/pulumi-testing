# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["NetworkContainerArgs", "NetworkContainer"]


class NetworkContainerArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas Network Container VPC` resource.
    """

    # required
    atlas_cidr_block: str
    project_id: Any

    # optional
    provider_name: Optional[str] = None
    region: Optional[str] = None
    region_name: Optional[str] = None
    regions: Optional[Sequence[str]] = None

    class Config:
        arbitrary_types_allowed = True


class NetworkContainer(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: NetworkContainerArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongo/alpha:NetworkContainer",
            name=f"{resource_name}-mongonetworkcontainer",
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
            self.net_container = mongodbatlas.NetworkContainer(
                resource_name=resource_name,
                atlas_cidr_block=args.atlas_cidr_block,
                project_id=args.project_id,
                provider_name=args.provider_name,
                region=args.region,
                region_name=args.region_name,
                regions=args.regions,
                opts=child_opts,
            )
        except Exception as ex:
            log.error(f"MongoNetworkContainer -> {ex.args[0]}")
        ###############################################################################
