import pyrax
import argparse

# Set your Rackspace credentials and parse arguments
USERNAME = "your_rackspace_username"
API_KEY = "your_rackspace_api_key"
REGION = "DFW"

# Set up argument parser
parser = argparse.ArgumentParser(description='Clean up Rackspace Cloud Files container')
parser.add_argument('--container-name', required=True, help='Name of the container to clean up')
parser.add_argument('--folder-prefix', default='', help='Folder path prefix to clean up (default: root)')
args = parser.parse_args()

# Authenticate
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credentials(USERNAME, API_KEY, region=REGION)

# Connect to Cloud Files
cf = pyrax.cloudfiles

# Get the container
container = cf.get_container(args.container_name)

# List objects in the folder
objs = container.get_objects(prefix=args.folder_prefix)

# Delete each object
for obj in objs:
    container.delete_object(obj.name)
    print(f"Deleted: {obj.name}")

print("Cleanup complete.")
# AI: make the CONTAINER_NAME be provided as an argument to this python script. Do not use sys.argv directly, use the best practice to parse parameters
