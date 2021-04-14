# Experiments

## Infrastructure required for experiments

Experiments can be conducted in Jupyter notebooks in Azure. These notebooks run on compute instances. Each data scientist will need to have his/her own compute instance to conduct experiments. 

To run experiments at scale, there needs to be at least 1 compute cluster for experimentation. Clusters can default to 0 nodes minimum to minimize cost. Data scientists can submit pipelines to run in compute clusters for experimentation.

## Reference ARM Templates for experiment resources
- [Compute Instance/Cluster](https://docs.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces/computes?tabs=json)


## Setup your compute instance to connect to your project repository in Azure DevOps

1. Start your compute instance. Do `Compute > Compute Instances > choose your instance > Start`
2. Open Terminal, either by clicking on `Terminal` for your instance or click on `JupyterLab > Launcher > $_ (Terminal)`
3. Create a key pair in Terminal. 
   ```
   $ ssh-keygen -t rsa
   ```
4. Copy contents of `~/.ssh/id_rsa.pub`
   ```
   $ cat ~/.ssh/id_rsa.pub
   ```
   Copy the text.
5. Go to Azure DevOps > User settings (upper right corner) > SSH Public Keys > New Key. Give it a name. Paste the contents of `id_rsa.pub` in Public Key Data.
6. Get your repository uri. `Azure DevOps > <Project Repo> > Clone (upper right) > SSH > copy icon`
6. Go back to Terminal. Navigate to your user directory. 
    ```
    $ cd ~/cloudfiles/code/Users/<yourUser>
    ```
7. Clone your repository.
    ```
    $ git clone <repository uri>
    ```
8. Create your notebooks in `<repository>/ml/experiments/notebooks`. 

**Notes**

*For NLP POC project, use path `huron/taxonomypoc/experiments`.*
*AzureML Python SDK and most common AI/ML Pyton packages are installed by default in the Compute Instance. To check `$ pip show <package name>`*