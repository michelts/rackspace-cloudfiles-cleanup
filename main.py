#!/usr/bin/env python3
import pyrax
import argparse
import logging
import asyncio

from pyrax.exceptions import ClientException


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger()


def get_cloudfiles_sdk(args):
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_credentials(args.username, args.api_key, region=args.region)
    return pyrax.cloudfiles


class ContainerDeleter:
    def __init__(self, cloudfiles_sdk, args):
        self.cloudfiles_sdk = cloudfiles_sdk
        self.args = args
        self.container = self.get_cloudfiles_container()

    def cleanup(self):
        logger.info("Starting cleanup")
        self.run_concurrent_delete(self.args.folder_prefix)
        try:
            self.container.delete()
        except ClientException:
            logger.info("Retry")
            self.run_concurrent_delete(self.args.folder_prefix)
            self.container.delete()
        logger.info("Cleanup complete")

    def get_cloudfiles_container(self):
        return self.cloudfiles_sdk.get_container(self.args.container_name)

    def run_concurrent_delete(self, prefix):
        objs = self.get_deleteable_objects(prefix)
        asyncio.run(self.delete_objects(objs))

    def get_deleteable_objects(self, prefix):
        return self.container.get_objects(prefix=prefix)

    async def delete_objects(self, objs):
        semaphore = asyncio.Semaphore(10)

        async def delete_single_object(obj_name):
            async with semaphore:
                try:
                    timeout_seconds = 5
                    await asyncio.wait_for(
                        asyncio.to_thread(self.container.delete_object, obj_name),
                        timeout=timeout_seconds,
                    )
                    logger.info(f"- deleted: {obj_name}")
                except asyncio.TimeoutError:
                    logger.error(f"Timeout deleting object: {obj_name}")
                except Exception as e:
                    logger.error(f"Error deleting object {obj_name}: {e}")

        # Create tasks for all objects
        tasks = [delete_single_object(obj.name) for obj in objs]

        # Wait for all tasks to complete with a global timeout of 5 minutes
        try:
            await asyncio.wait_for(asyncio.gather(*tasks), timeout=300.0)
        except asyncio.TimeoutError:
            logger.error("Global timeout reached while deleting objects")


def list_containers(cloudfiles_sdk):
    containers = cloudfiles_sdk.list()
    logger.info("Available containers:")
    for container in containers:
        logger.info(container.name)


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
        deleter = ContainerDeleter(cloudfiles_sdk, args)
        deleter.cleanup()
