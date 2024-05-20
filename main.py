from azure.identity import *
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.fileshare import ShareClient, ShareServiceClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
import random
import defaults
import importlib
import time

def ResourceGroup(credential,subscription_id):
    resource_client = ResourceManagementClient(credential,subscription_id)
    resourcegroup = resource_client.resource_groups.create_or_update(
        'project-resource-group',
        {'location':defaults.DEFAULT_LOCATION_RESOURCE_GROUP}
    )
    return resourcegroup.name


def StorageGroup(resource_group,credential,subscription_id):
     
    storage_client = StorageManagementClient(credential,subscription_id)                     #Setting up storage management client
    var= False
    while var != True:
        Base_name = f'{'projectstorageaccount'}{random.randint(1,100)}'                           #Checking the availability of the storage group name
        result = storage_client.storage_accounts.check_name_availability({'name':Base_name})
        var = result.name_available

    poller = storage_client.storage_accounts.begin_create(
        resource_group_name = resource_group, account_name = Base_name ,                      #Creating storage group with a unique name
        parameters = { 'location': defaults.DEFAULT_LOCATION , 'kind': 'StorageV2' , 'sku' : {'name' : 'Standard_LRS'}
                    }
    )

    poller_Results = poller.result()
    storage_account =  poller_Results.name
    return storage_account

def FileShare():
    connection_string = input("Input the connection string for the storage account")
    share_service_client = ShareServiceClient.from_connection_string(connection_string)
    share_client_1 = share_service_client.create_share(share_name="location1-share")
    share_client_2 = share_service_client.create_share(share_name="location2-share")


def BranchEndPoints(resource_group,credential,subscription,VNET_NAME,SUBNET_NAME,IP_NAME,NIC_NAME):
    network_client = NetworkManagementClient(credential, subscription)                       #Setting up Network Management Client
    poller = network_client.virtual_networks.begin_create_or_update(                         #Setting up the virtual network
        resource_group_name = resource_group, 
        virtual_network_name = VNET_NAME,
        parameters = {'location': 'eastus',
                     'address_space': {
                         'address_prefixes': ['10.0.0.0/16']
                     }
                     }
    )
    result = poller.result()
    
    poller = network_client.subnets.begin_create_or_update(                                  #Setting up the subnet
        resource_group_name = resource_group, 
        virtual_network_name = VNET_NAME,
        subnet_name= SUBNET_NAME,
        subnet_parameters = {'address_prefixes': ['10.0.0.0/24']
                     }
                     
    )
    result = poller.result()
    result.provisioning_state
    
    poller = network_client.public_ip_addresses.begin_create_or_update(                      #Setting up public ip address
        resource_group_name = resource_group,
        public_ip_address_name = IP_NAME, 
        parameters= {'location': 'eastus', 'sku' : {'name': 'Standard'}, 'public_ip_allocation_method' : 'Static', 
                     'public_ip_address_version' :'IPV4'}
    )
    ip_result = poller.result()
    ip_result.provisioning_state
    ip_result.name
    ip_result.ip_address
    
    poller = network_client.network_interfaces.begin_create_or_update(                        #Setting up a network interface client
        resource_group_name = resource_group, network_interface_name = NIC_NAME , 
        parameters= {'location': 'eastus', 'ip_configurations':[{'name' : 'test-ip-config' , 
                                                                 'subnet' : {'id':result.id}, 
                                                                 'public_ip_address':{'id' :ip_result.id}}] }
        
    )
    nic_results = poller.result()
    return (nic_results)

def VM_development(resource_group,VM_NAME,nic,credential,subscription):
    compute_client = ComputeManagementClient(credential, subscription)                         #Creation of VM
    poller = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name = resource_group,
        vm_name= VM_NAME,
        parameters= {
        'location': 'eastus', 
        'storage_profile' : {
            'image_reference': {'publisher': 'MicrosoftWindowsServer','offer': 'WindowsServer','sku': '2019-Datacenter','version': 'latest' }
        },
        'hardware_profile': {'vm_size':'Standard_DS1_v2' }, 
        'os_profile' : {'computer_name':VM_NAME, 'admin_username': 'testuser', 'admin_password':'Password@18100'}, 
        'network_profile': {
            'network_interfaces': [ {'id':nic.id}]
        }
    }
    )

if __name__ == "__main__":
    subscription_id = defaults.DEFAULT_SUBSCRIPTION
    credential = AzureCliCredential()
    resource_group = ResourceGroup(credential,subscription_id)
    storage_account = StorageGroup(resource_group,credential,subscription_id)
    FileShare()
    VM_NAME_1 = defaults.VM_NAME_1
    VM_NAME_2 = defaults.VM_NAME_2
    nic_1 = BranchEndPoints(resource_group,credential,subscription_id,defaults.VNET_NAME_1,defaults.SUBNET_NAME_1,defaults.IP_NAME_1,defaults.NIC_NAME_1)
    VM_development(resource_group,VM_NAME_1,nic_1,credential,subscription_id)
    nic_2 = BranchEndPoints(resource_group,credential,subscription_id,defaults.VNET_NAME_2,defaults.SUBNET_NAME_2,defaults.IP_NAME_2,defaults.NIC_NAME_2)
    VM_development(resource_group,VM_NAME_2,nic_2,credential,subscription_id)
    
    
