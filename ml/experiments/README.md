# Experimentation

## Infrastructure required for experimentation

Experimentation can be conducted in Jupyter notebooks in Azure. These notebooks run on compute instances. Each data scientist will need to have his/her own compute instance to conduct experiments. 

To run experiments at scale, there needs to be at least 1 compute cluster for experimentation. Clusters can default to 0 nodes minimum to minimize cost. Data scientists can submit pipelines to run in compute clusters for experimentation.

### Setup

1. Update `ml/experiments/infra.json`


## Reference ARM Templates for experimentation resources
- [Compute Instance/Cluster](https://docs.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces/computes?tabs=json)