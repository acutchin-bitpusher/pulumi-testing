# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["DbUserArgs", "DbUser"]


class DbUserArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas DB User` resource.
    """

    # required
    project_id: Any
    username: str
    roles: Optional[Sequence[mongodbatlas.DatabaseUserRoleArgs]] = None
    auth_database_name: Optional[str] = None
    password: Optional[str] = None

    # optional
    labels: Optional[Sequence[mongodbatlas.DatabaseUserLabelArgs]] = None
    scopes: Optional[Sequence[mongodbatlas.DatabaseUserScopeArgs]] = None

    class Config:
        arbitrary_types_allowed = True


class DbUser(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: DbUserArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongo/alpha:MongoDbUser",
            name=f"{resource_name}-mongodbuser",
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
            mongodbatlas.DatabaseUser(
                resource_name=resource_name,
                project_id=args.project_id,
                username=args.username,
                roles=args.roles,
                auth_database_name=args.auth_database_name,
                password=args.password,
                labels=args.labels,
                scopes=args.scopes,
                opts=child_opts,
            )
        except Exception as ex:
            log.error(f"MongoDbUser -> {ex.args[0]}")
        ###############################################################################
