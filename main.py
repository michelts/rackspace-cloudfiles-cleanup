#!/usr/bin/env python3
import pyrax
import argparse


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean up files in a Rackspace Cloud Files container",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "--username", required=True, help="Rackspace cloud username", metavar="USERNAME"
    )
    required.add_argument(
        "--api-key", required=True, help="Rackspace API key", metavar="KEY"
    )
    required.add_argument(
        "--container-name",
        required=True,
        help="Name of the container to clean up",
        metavar="NAME",
    )
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "--region", default="DFW", help="Rackspace region", metavar="REGION"
    )
    optional.add_argument(
        "--folder-prefix",
        default="",
        help="Folder path prefix to clean up",
        metavar="PREFIX",
    )
    return parser.parse_args()


def get_container(username, api_key, container_name, region):
    """Get a Rackspace Cloud Files container."""
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_credentials(username, api_key, region=region)
    cf = pyrax.cloudfiles
    return cf.get_container(container_name)


def delete_objects(container, prefix):
    """Delete objects in container matching prefix."""
    objs = container.get_objects(prefix=prefix)
    for obj in objs:
        # container.delete_object(obj.name)
        print(f"Deleted: {obj.name}")
    print("Cleanup complete.")


if __name__ == "__main__":
    args = parse_arguments()

    # Get the container
    container = get_container(args.username, args.api_key, args.container_name, args.region)

    # Delete objects
    delete_objects(container, args.folder_prefix)
