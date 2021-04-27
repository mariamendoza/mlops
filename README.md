[![Build Status](https://dev.azure.com/auimendoza/pipelines-azureml/_apis/build/status/mlops?branchName=master)](https://dev.azure.com/auimendoza/pipelines-azureml/_build/latest?definitionId=3&branchName=master)

# MLOps

## Azure ML Workspace

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

## Azure ML Workspace Architecture

Azure ML Workspace is needed on all environments dev, qa and prod. Dev is primarily for experimentation and training. QA and Prod are primarily for serving preprocessing (optional) and scoring endpoints. All environments should have access to raw data sources that have PROD-quality data. If these data sources are found in prod storage accounts, or storage accounts in other resource groups or subscriptions, then these storage accounts must be added as a datastore in Azure ML Workspace.

![](docs/images/AzureML-dev.png)

In the dev workspace, experiments are conducted in compute instances to provide sufficient resources for processing data in a small to medium scale. Large scale data processing and training run on compute clusters. Pipelines with endpoints can be setup to allow triggering of these pipelines from within experiments or within cicd pipelines. Scoring pipelines can be deployed in dev for the purpose of testing.

![](docs/images/AzureML-qa-prod.png)

QA and PROD environments are setup to include preprocessing and scoring pipelines only. Preprocessing pipelines are optional and is necessary only if client will need a way to format its raw data to a form acceptable to the model in the scoring pipeline. Datastores are defined as needed.

## DevOps Process


## Repository Structurels