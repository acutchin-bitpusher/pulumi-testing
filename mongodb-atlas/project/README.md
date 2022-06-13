# DevOps Pulumi GCP Infra Resources example

This folder contains an example Pulumi program which demonstrates use of the `devops_plm_gcp_infra` package.

_*TODO: Update this project with an example, and provide an explaination here.*_

## Getting started

To run this example:

* Install and start a VirtualEnv in this folder
* Locally install (or reinstall) the `devops_plm_gcp_infra` package from the root directory:

```
pip install -e ..
```

* Optionally set your provider configuration:

```
pulumi config set provider_param_1 [value]
pulumi config set provider_param_2 [value]
```

* Pulumi

- Select/Create: `$ pulumi stack select <stack> --create`
- Preview: `$ pulumi preview -s <stack>`
- Apply: `$ pulumi up -s <stack>`
