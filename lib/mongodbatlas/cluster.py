# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

import pulumi_mongodbatlas as mongodbatlas
from pulumi import ComponentResource, ResourceOptions, log
from pydantic import BaseModel

# from ... import _utilities

__all__ = ["ClusterArgs", "Cluster"]


class ClusterArgs(BaseModel):
    """
    The arguments necessary to construct a `MongoDB Atlas Cluster` resource.
    """

    # required
    project_id: Any
    provider_instance_size_name: str
    provider_name: str
    backing_provider_name: str = None
    auto_scaling_disk_gb_enabled: bool

    # optional
    auto_scaling_compute_enabled: Optional[bool] = None
    auto_scaling_compute_scale_down_enabled: Optional[bool] = None
    provider_auto_scaling_compute_max_instance_size: Optional[str] = None
    provider_auto_scaling_compute_min_instance_size: Optional[str] = None
    name: Optional[str] = None
    cloud_backup: Optional[bool] = None
    disk_size_gb: Optional[float] = None
    cluster_type: Optional[str] = None
    provider_region_name: Optional[str] = None
    mongo_db_major_version: Optional[str] = None
    pit_enabled: Optional[bool] = None
    provider_disk_iops: Optional[int] = None
    provider_volume_type: Optional[str] = None
    replication_factor: Optional[int] = None
    replication_specs: Optional[
        Sequence[mongodbatlas.ClusterReplicationSpecArgs]
    ] = None

    class Config:
        arbitrary_types_allowed = True


class Cluster(ComponentResource):
    def __init__(
        self,
        resource_name: str,
        args: ClusterArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__(
            t="devops-plm-gcp-infra:mongo/alpha:MongoDbCluster",
            name=f"{resource_name}-mongodbcluster",
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
            self.cluster = mongodbatlas.Cluster(
                resource_name=resource_name,
                project_id=args.project_id,
                provider_instance_size_name=args.provider_instance_size_name,
                provider_name=args.provider_name,
                backing_provider_name=args.backing_provider_name,
                auto_scaling_disk_gb_enabled=args.auto_scaling_disk_gb_enabled,
                auto_scaling_compute_enabled=args.auto_scaling_compute_enabled,
                auto_scaling_compute_scale_down_enabled=args.auto_scaling_compute_scale_down_enabled,
                provider_auto_scaling_compute_max_instance_size=args.provider_auto_scaling_compute_max_instance_size,
                provider_auto_scaling_compute_min_instance_size=args.provider_auto_scaling_compute_min_instance_size,
                name=args.name,
                disk_size_gb=args.disk_size_gb,
                cloud_backup=args.cloud_backup,
                cluster_type=args.cluster_type,
                provider_region_name=args.provider_region_name,
                mongo_db_major_version=args.mongo_db_major_version,
                pit_enabled=args.pit_enabled,
                provider_disk_iops=args.provider_disk_iops,
                provider_volume_type=args.provider_volume_type,
                replication_factor=args.replication_factor,
                replication_specs=args.replication_specs,
                opts=child_opts,
            )
        except Exception as ex:
            log.error(f"MongoDbCluster -> {ex.args[0]}")
        ###############################################################################
