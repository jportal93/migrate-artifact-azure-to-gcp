import os
import re
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from google.cloud import storage
from google.oauth2 import service_account

# Path to the service account JSON file
key_path = "./prod.json"

##############
#you can get this info in the secret
azure_registry = 'containers.azurecr.io'
azure_user = 'userContainers'
azure_password = '...........'

#  Google info
google_region = 'us-central1'
google_project_id = 'project_id'
google_repository = 'name_of_repository_in_artifact'

parth_artifact = "us-east1-docker.pkg.dev/{google_project_id}/path"
############

def find_images_with_prefix(directory, prefix):
    images_with_prefix = []
    pattern = re.compile(r'\b' + re.escape(prefix) + r'[^\s,]+')

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        match = pattern.search(line)
                        if match:
                            images_with_prefix.append(match.group())

    return images_with_prefix

# Gitops files directory
directory_path = '/Users/jportal/Documents/GitHub/kubernetes-gitops/'

# Azure Container Registry Image Prefix
prefix = 'containers.azurecr.io/'

# Find the lines with images in the gitops files
images = find_images_with_prefix(directory_path, prefix)

# Print matches
print("images:")
for image in images:
    print(image)



def setup_auth():
    # Auth in Azure
    os.system(f'docker login {azure_registry} -u {azure_user} -p {azure_password}')
    
    # Auth google 
    #os.system('gcloud auth login')
    #os.system(f'gcloud auth configure-docker {google_region}-docker.pkg.dev')

setup_auth()




# Sets the environment variable for service account authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    key_path,
)
i=0
for image in images:
    #setup_auth()
    os.system(f'docker pull {image}')
    i = i +1
    full_image_path = image
    image_name_tag = image.split('/')[-1]
    image_name = image_name_tag.split(':')[0]
    tag = image_name_tag.split(':')[1]
    print(image_name)
    
    os.system("gcloud auth configure-docker us-east1-docker.pkg.dev --quiet")
    os.system(f'docker tag {azure_registry}/{image_name}:{tag} {parth_artifact}/{image_name}:{tag}')
    os.system(f'docker push {parth_artifact}/{image_name}:{tag}')
    # Full image paths for Google
    os.system(f'docker rmi {full_image_path}')
    os.system(f'docker rmi {parth_artifact}/{image_name}:{tag}')




