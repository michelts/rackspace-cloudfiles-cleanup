#!/usr/bin/env python3
import pyrax
import argparse


class Parser:
    def __init__(self, args):
        self.args = args
        self.container = self.get_cloudfiles_container()

    def cleanup(self):
        print("Starting cleanup")
        self.delete_objects(self.args.folder_prefix)
        self.container.delete()
        print("Cleanup complete")

    def get_cloudfiles_container(self):
        pyrax.set_setting("identity_type", "rackspace")
        pyrax.set_credentials(
            self.args.username, self.args.api_key, region=self.args.region
        )
        return pyrax.cloudfiles.get_container(self.args.container_name)

    def delete_objects(self, prefix):
        objs = self.container.get_objects(prefix=prefix)
        for obj in objs:
            self.container.delete_object(obj.name)
            print(f"- deleted: {obj.name}")


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


if __name__ == "__main__":
    args = parse_arguments()
    parser = Parser(args)
    parser.cleanup()
    print("Container deleted.")
