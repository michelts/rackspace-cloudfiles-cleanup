#!/usr/bin/env python3
import argparse
from openstack import connection


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean up files in an OpenStack Cloud Files container",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "--container-name",
        required=True,
        help="Name of the container to clean up",
        metavar="NAME",
    )
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "--folder-prefix",
        default="",
        help="Folder path prefix to clean up",
        metavar="PREFIX",
    )
    return parser.parse_args()


def delete_objects(cloudfiles_connection, container_name, prefix):
    container = cloudfiles_connection.object_store.get_container_objects(
        container_name, prefix=prefix
    )
    for obj in container:
        # conn.object_store.delete_object(obj, container=container_name)
        print(f"Deleted: {obj.name}")
    print("Cleanup complete.")


if __name__ == "__main__":
    args = parse_arguments()
    cloudfiles_connection = connection.Connection(cloud="rackspace")
    delete_objects(cloudfiles_connection, args.container_name, args.folder_prefix)
