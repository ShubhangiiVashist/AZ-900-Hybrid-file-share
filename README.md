# Project for AZ-900 - Implement Hybrid file share with disaster recovery

Hi, my intention in developing these projects is to make learning enjoyable. By examining real-life implementations of cloud services, you can gain a deeper understanding of the concepts, making learning more engaging and aiding in better retention of the material, which is beneficial for passing the AZ-900 exam.

In this project, we implement a simple architecture of a Hybrid File share using Python SDK as well as the Azure portal.  

## Azure Services that you will learn
- Azure Storage
- Azure File Share service
- Azure File Sync service
- Azure Virtual machine

## Architecture 

![diagram](Architecture-az.jpg)

- GitHub for Version control.
- Azure Storage account to deploy file share in both branches.
- Azure File Share to provide a cloud platform for the files to sync from the on-premise servers.
- Azure Storage sync service to deploy file sync service.
- Virtual machine to simulate the on-premise servers.
- Azure file sync agent to create a server endpoint on the virtual machine. 
- [Python](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview) for our Infrastructure as Code.

## You'll need

- [Azure account](azure.com/free)
- [GitHub account](github.com/join)
- Prerequisite: Azure subscription

For local developer environment

- VS Code/ Jupyter notebook
- Docker (optional)

## How to get started

### Authenticate your Environment with Azure
In the Terminal, type `az login --use-device-code` to log into your Azure account from the az cli.

### Get the code and environment

1. [Fork the repository](https://docs.github.com/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) so you can have your own copy of it. 
2. If you don't already have Jupyter notebook installed, navigate to [python](https://jupyter.org/) and download the latest version. Follow the installation instructions for the setup.
3. Launch Jupyter Notebook and open [main.py](main.py) and [defaults.py](defaults.py). 
4. Replace the parameters in [defaults.py](defaults.py) with your own. You can modify the other default parameters or leave them as it is(your choice).
5. Now execute main.py to build the sample architecture.

### How the codebase works
The code base will create the following component with the required configurations : 
- A resource group in Central India location (can be modified in defaults.py)
- A storage group in South India location (can be modified in defaults.py)
- Two file shares in the storage group one for each branch
- Two virtual machines in East US (can be modified in defaults.py)

### Manual setup to complete the architecture 

- **Steps**:
   1. **Prepare Windows Server to use with Azure File Sync**:
        - For each server disable Internet Explorer Enhanced Security Configuration. This is required only for initial server registration. You can re-enable it after the server has been registered.
        - [See the steps here](https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-deployment-guide?tabs=azure-portal%2Cproactive-portal#prepare-windows-server-to-use-with-azure-file-sync)
   2. **Install the Azure File Sync agent**:
        - The Azure File Sync agent is a downloadable package that enables Windows Server to be synced with an Azure file share.
        - You can download the agent from the [Microsoft Download Center](https://go.microsoft.com/fwlink/?linkid=858257). When the download is finished, double-click the MSI package to start the Azure File Sync agent installation.
   
   3. **Register Windows Server with Storage Sync Service**:
        - The Server Registration UI should open automatically after installation of the Azure File Sync agent. If it doesn't, you can open it manually from its file location: C:\Program Files\Azure\StorageSyncAgent\ServerRegistration.exe.
        - Fill out the appropriate information to register the server. 
   
   4. **Create a sync group and a cloud endpoint**:
        - A sync group defines the sync topology for a set of files. Endpoints within a sync group are kept in sync with each other. A sync group must contain one cloud endpoint, which represents an Azure file share that we created using the code base and one or more server endpoints.
        - For this project we will create two different sync groups, one for each branch. Each sync group has one cloud endpoint which refers to the fileshare we have created.
        - Refer [here](https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-deployment-guide?tabs=azure-portal%2Cproactive-portal#create-a-sync-group-and-a-cloud-endpoint) to understand the creation of sync group and cloud endpoint.
          
      5. **Create a server endpoint**:
         -  A server endpoint represents a path on a registered server say D:\data where "data" is the folder you have created in the D drive of the server. The files from this folder will be synced to the file share.
         -  A sync group can have multiple server endpoints but in this project we will assign one server to each sync group, which would represent one branch.
         - Refer [here](https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-deployment-guide?tabs=azure-portal%2Cproactive-portal#create-a-server-endpoint) to understand the creation of server endpoint.

Post the creation of all the components, you can try uploading files on the virtual machines(which represents on-prem workstations) and see how they are getting synced into the fileshare. Also the clients can directly access the fileshares using the publicly accessible links. 

        
