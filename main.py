#!/usr/bin/env python3
import argparse
from openstack import connection


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean up files in an OpenStack Cloud Files container",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument(
        "--container-name",
        required=True,
        help="Name of the container to clean up",
        metavar="NAME",
    )

    optional.add_argument(
        "--folder-prefix",
        default="",
        help="Folder path prefix to clean up",
        metavar="PREFIX",
    )
    return parser.parse_args()


def delete_objects(conn, container_name, prefix):
    """Delete objects in container matching prefix."""
    container = conn.object_store.get_container_objects(container_name, prefix=prefix)
    
    for obj in container:
        # conn.object_store.delete_object(obj, container=container_name)
        print(f"Deleted: {obj.name}")
    print("Cleanup complete.")


if __name__ == "__main__":
    args = parse_arguments()
    
    # Create connection using standard OpenStack environment variables
    conn = connection.Connection(cloud='rackspace')
    
    # Delete matching objects
    delete_objects(conn, args.container_name, args.folder_prefix)
# AI: make the CONTAINER_NAME be provided as an argument to this python script. Do not use sys.argv directly, use the best practice to parse parameters
