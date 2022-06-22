# -*- coding: utf-8 -*-

from typing import Optional, Sequence

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["ProjectArgs", "Project"]


class ProjectArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas Project` resource.
    """

    # required
    name: str
    org_id: str

    # optional
    teams: Optional[Sequence[mongodbatlas.ProjectTeamArgs]] = None

    class Config:
        arbitrary_types_allowed = True


class Project(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: ProjectArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongodbatlas/alpha:Project",
            name=f"{resource_name}-mongoproject",
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
            self.project = mongodbatlas.Project(
                resource_name=resource_name,
                name=args.name,
                org_id=args.org_id,
                teams=args.teams,
                opts=child_opts,
            )
        except Exception as ex:
            log.error(f"MongoProject -> {ex.args[0]}")
        ###############################################################################
