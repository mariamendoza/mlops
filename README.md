[![Build Status](https://dev.azure.com/auimendoza/pipelines-azureml/_apis/build/status/mlops?branchName=master)](https://dev.azure.com/auimendoza/pipelines-azureml/_build/latest?definitionId=3&branchName=master)

## Azure ML MLOps

### Required resources:

1. Key Vault
4. Container Registry
2. Application Insights
3. Storage Account

### Key Vault

MLOps can share KeyVault resource.  KeyVault names are global.

### Storage Account

Use general purpose v2 storage account. Storage account names are global. MLOps will use its own storage account for storing:

1. Pipeline generated artifacts such as:
    1. logs
    1. model pickle files
    1. pipeline data
2. Registered datasets

### Application Insights

Application Insights allows monitoring of applications running inside containers. This would be used by Azure ML Pipelines running in Azure container instances (ACI) or in Azure Kubernetes Service (AKS).

### Container Registry

Container Registry is an optional component in an MLOps project. It will be needed only when the ml ops process requires creating its own custom container image. Container registry can be shared.

## DevOps Process

[](docs/images/AzureML-dev.png)

()[docs/images/AzureML-qa-prod.png]

## Repository Structure