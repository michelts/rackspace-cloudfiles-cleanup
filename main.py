#!/usr/bin/env python3
import pyrax
import argparse


def get_cloudfiles_sdk(args):
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_credentials(args.username, args.api_key, region=args.region)
    return pyrax.cloudfiles


class Parser:
    def __init__(self, cloudfiles_sdk, args):
        self.cloudfiles_sdk = cloudfiles_sdk
        self.args = args

    def cleanup(self):
        print("Starting cleanup")
        container = self.get_cloudfiles_container()
        self.delete_objects(container, self.args.folder_prefix)
        container.delete()
        print("Cleanup complete")

    def get_cloudfiles_container(self):
        return self.cloudfiles_sdk.get_container(self.args.container_name)

    def delete_objects(self, container, prefix):
        objs = container.get_objects(prefix=prefix)
        for obj in objs:
            container.delete_object(obj.name)
            print(f"- deleted: {obj.name}")


def list_containers(cloudfiles_sdk):
    containers = cloudfiles_sdk.list()
    print("Available containers:")
    for container in containers:
        print(container.name)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean up files in a Rackspace Cloud Files container or list containers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "--username", required=True, help="Rackspace cloud username", metavar="USERNAME"
    )
    required.add_argument(
        "--api-key", required=True, help="Rackspace API key", metavar="KEY"
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
    optional.add_argument(
        "--container-name",
        help="Name of the container to clean up",
        metavar="NAME",
    )
    optional.add_argument(
        "--list-containers", action="store_true", help="List all containers"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    cloudfiles_sdk = get_cloudfiles_sdk(args)
    if args.list_containers:
        list_containers(cloudfiles_sdk)
    else:
        parser = Parser(cloudfiles_sdk, args)
        parser.cleanup()
