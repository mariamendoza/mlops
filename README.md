# mlops

## Required resources:

1. Key Vault
4. Container Registry
2. Application Insights
3. Storage Account

## Key Vault

MLOps will use its own Key Vault as per [Key Vault Best Practices Dcumentation](https://docs.microsoft.com/en-us/azure/key-vault/general/best-practices). KeyVault names are global.

### Recommended Settings:

1. use RBAC
2. Turn on Firewall and VNET Service Endpoints
3. Turn on logging and alerts
4. Turn on soft delete
5. Turn on purge protection for PROD

## Storage Account

Use general purpose v2 storage account. Refer to this [documentation](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview?toc=/azure/storage/blobs/toc.json). Storage account names are global.

MLOps will use its own storage account for storing:

1. Pipeline generated artifacts such as:
  1. logs
  2. pickle files
2. Processed datasets

### Recommended settings:

1. use security groups instead of individual users
2. use service principals for Azure services access
3. enable Firewall with Azure service access

## Application Insights

Application Insights allows monitoring of applications running inside containers. This would be used by Azure ML Pipelines running in Azure container instances (ACI) or in Azure Kubernetes Service (AKS).
For more information, refer to (documentation)[https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview]

## Container Registry

Container Registry is an optional component in an MLOps project. It will be needed only when the ml ops process requires creating its own custom container image. 

As per (best practice)[https://docs.microsoft.com/en-us/azure/container-registry/container-registry-best-practices], container registries can be shared and should be in its own resource group where it can be centrally managed. 

User RBAC for access control to the container registry. Service principal access for CI/CD is sufficient for MLOps.

### Naming Restrictions

Product | Global Name | Length | Valid Characters 
--|--|--|--
ML Workspace | No | 3-33 chars| alphanumeric, hyphen, underscore
Storage Account |Yes |3-24 chars | lowercase, numbers
Key Vault | Yes |3-24 chars| alphanumeric, dash, start with letter, end with letter or digit, non-consecutive hyphens
Application Insights |No|1-255 chars| alphanumeric, period, underscore, hyphen, parenthesis, cannot end in period
Container Registry |Yes|5-50 chars|alphanumeric