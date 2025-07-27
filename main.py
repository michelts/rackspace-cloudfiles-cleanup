import pyrax

# Set your Rackspace credentials
USERNAME = "your_rackspace_username"
API_KEY = "your_rackspace_api_key"
REGION = "DFW"
CONTAINER_NAME = "your_container"
FOLDER_PREFIX = "your/folder/path/"  # e.g., "backups/old/"

# Authenticate
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credentials(USERNAME, API_KEY, region=REGION)

# Connect to Cloud Files
cf = pyrax.cloudfiles

# Get the container
container = cf.get_container(CONTAINER_NAME)

# List objects in the folder
objs = container.get_objects(prefix=FOLDER_PREFIX)

# Delete each object
for obj in objs:
    container.delete_object(obj.name)
    print(f"Deleted: {obj.name}")

print("Cleanup complete.")
