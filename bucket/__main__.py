import pulumi
import pulumi_gcp as gcp

config = pulumi.Config()
pulumi_stack_name = pulumi.get_stack()
pulumi_project_name = pulumi.get_project()
print( "   pulumi_stack_name: ", pulumi_stack_name )
print( " pulumi_project_name: ", pulumi_project_name )

resource_name_prefix = pulumi_project_name + "_" + pulumi_stack_name
print( "resource_name_prefix: ", resource_name_prefix )

env_config = config.require_object("env_config")

bucket_name = resource_name_prefix + "_" + env_config["unique_string"] + "_bucket"
print( "         bucket_name: ", bucket_name )

##  https://www.pulumi.com/registry/packages/gcp/api-docs/storage/bucket/
bucket = gcp.storage.Bucket(
  bucket_name,
  #location='US'
  location=env_config["gcp_region"]
)

print( "          bucket_url: ", bucket.url )

pulumi.export( 'bucket_url', bucket.url )
