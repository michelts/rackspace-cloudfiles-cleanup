import pyrax
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Clean up Rackspace Cloud Files container"
    )
    parser.add_argument("--username", required=True, help="Rackspace cloud username")
    parser.add_argument("--api-key", required=True, help="Rackspace API key")
    parser.add_argument("--region", default="DFW", help="Rackspace region (default: DFW)")
    parser.add_argument(
        "--container-name", required=True, help="Name of the container to clean up"
    )
    parser.add_argument(
        "--folder-prefix",
        default="",
        help="Folder path prefix to clean up (default: root)",
    )
    return parser.parse_args()


args = parse_arguments()

# Authenticate
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_credentials(args.username, args.api_key, region=args.region)

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
