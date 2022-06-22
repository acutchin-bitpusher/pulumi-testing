# -*- coding: utf-8 -*-
from typing import Any, Mapping, Optional, Sequence, Union

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["TeamArgs", "Team"]


class TeamArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas Team` resource.
    """

    # required
    name: str
    org_id: str
    usernames: Sequence[str]

    # optional

    class Config:
        arbitrary_types_allowed = True


class Team(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: Sequence[Union[TeamArgs, Mapping[str, Any]]],
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongodbatlas/alpha:Team",
            name=f"{resource_name}-mongodbteam",
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
            self.created_teams = []
            for i, team in enumerate(args):
                if not isinstance(team, TeamArgs):
                    team = TeamArgs(**team)
                team_ = mongodbatlas.Team(
                    resource_name=f"{resource_name}-{i}",
                    name=team.name,
                    org_id=team.org_id,
                    usernames=team.usernames,
                    opts=child_opts,
                )
                self.created_teams.append(team_)
        except Exception as ex:
            log.error(f"MongoDbTeam -> {ex.args[0]}")
        ###############################################################################
