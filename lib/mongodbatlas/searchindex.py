# -*- coding: utf-8 -*-

from typing import Optional

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["IndexArgs", "Index"]


class IndexArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas SearchIndex` resource.
    """

    # required
    analyzer: str
    cluster_name: str
    collection_name: str
    database: str
    name: str
    project_id: str
    mappings_dynamic: bool

    # optional

    class Config:
        arbitrary_types_allowed = True


class Index(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: IndexArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongodbatlas/alpha:Index",
            name=f"{resource_name}-mongodbindex",
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
            mongodbatlas.SearchIndex(
                resource_name=resource_name,
                name=args.name,
                analyzer=args.analyzer,
                cluster_name=args.cluster_name,
                collection_name=args.collection_name,
                database=args.database,
                project_id=args.project_id,
                mappings_dynamic=args.mappings_dynamic,
                opts=child_opts,
            )
        except Exception as ex:
            log.error(f"MongoDbIndex -> {ex.args[0]}")
        ###############################################################################
