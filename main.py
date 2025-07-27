import pyrax
import argparse


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean up files in a Rackspace Cloud Files container",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    required.add_argument("--username", required=True, 
                         help="Rackspace cloud username", metavar="USERNAME")
    required.add_argument("--api-key", required=True,
                         help="Rackspace API key", metavar="KEY")
    required.add_argument("--container-name", required=True,
                         help="Name of the container to clean up", metavar="NAME")
    
    optional.add_argument("--region", default="DFW", 
                         help="Rackspace region", metavar="REGION")
    optional.add_argument("--folder-prefix", default="",
                         help="Folder path prefix to clean up", metavar="PREFIX")
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
    # container.delete_object(obj.name)
    print(f"Deleted: {obj.name}")

print("Cleanup complete.")
# AI: make the CONTAINER_NAME be provided as an argument to this python script. Do not use sys.argv directly, use the best practice to parse parameters
