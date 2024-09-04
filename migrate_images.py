import os
import re
import subprocess
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from google.cloud import storage
from google.oauth2 import service_account

# Path to the service account JSON file
key_path = "./prod.json"

##############
# You can get this info in the secret
azure_registry = 'containers.azurecr.io'
azure_user = 'userContainers'
azure_password = '********'

# Google info
google_region = 'us-central1'
google_project_id = 'project_id'
google_repository = 'name_of_repository_in_artifact'

# Fixed string formatting using f-string
path_artifact = f"us-east1-docker.pkg.dev/{google_project_id}/path"
############


def find_images_with_prefix(directory, prefix):
    """Find images in YAML files with a given prefix."""
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


def setup_auth():
    """Authenticate with Azure and Google Container Registries."""
    try:
        # Authenticate in Azure
        subprocess.run(
            ['docker', 'login', azure_registry, '-u', azure_user, '-p', azure_password],
            check=True
        )
        print("Authenticated to Azure successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to authenticate to Azure: {e}")


# GitOps files directory
directory_path = '/Users/jportal/Documents/GitHub/kubernetes-gitops/'

# Azure Container Registry Image Prefix
prefix = 'containers.azurecr.io/'

# Find the lines with images in the GitOps files
images = find_images_with_prefix(directory_path, prefix)

# Print matches
print("Images found:")
for image in images:
    print(image)


# Sets the environment variable for service account authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# Load credentials
credentials = service_account.Credentials.from_service_account_file(key_path)

# Authenticate with Azure and Google
setup_auth()

i = 0
for image in images:
    try:
        # Pull the image from Azure
        subprocess.run(['docker', 'pull', image], check=True)
        i += 1
        full_image_path = image
        image_name_tag = image.split('/')[-1]
        image_name = image_name_tag.split(':')[0]
        tag = image_name_tag.split(':')[1]

        print(f"Processing image: {image_name}")

        # Tag the image for Google Artifact Registry
        subprocess.run(
            ['docker', 'tag', f'{azure_registry}/{image_name}:{tag}', f'{path_artifact}/{image_name}:{tag}'],
            check=True
        )

        # Push the image to Google Artifact Registry
        subprocess.run(['docker', 'push', f'{path_artifact}/{image_name}:{tag}'], check=True)

        # Clean up local images
        subprocess.run(['docker', 'rmi', full_image_path], check=True)
        subprocess.run(['docker', 'rmi', f'{path_artifact}/{image_name}:{tag}'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to process image {image_name}: {e}")
