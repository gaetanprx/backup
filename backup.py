#!/usr/bin/python

import argparse
import datetime
import os
import shutil
import yaml


def get_argument_parser():
    parser = argparse.ArgumentParser(description="Script to backup")
    parser.add_argument("--config", help="config is in the yaml file", required=True)
    return parser


# A function to read yaml file
def read_yaml(yaml_file_path: str) -> dict:
    wit open(yaml_file_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as exc:
            print(exc)


def does_exist(path: str):
    return os.path.exists(path)


# Check if the destination path exist
def check_exist(path: str, create_if_not_exist: bool = False):
    if not does_exist(path):
        if create_if_not_exist:
            print(f"path {path} has been created")
            os.mkdir(path)
        else:
            raise Exception(f"path {path} does not exist")


def create_full_path_backup(path: str) -> str:
    backup_folder = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    full_path = os.path.join(path, backup_folder)
    check_exist(full_path, create_if_not_exist=True)
    return full_path


def full_copy_files(
    src_path: str,
    dest_path: str,
    symlinks=False,
    ignore=None
):
    # Copy each file from src dir to dest dir, include sub-directories.
    for item in os.listdir(src_path):
        file_path = os.path.join(src_path, item)
        new_dest = os.path.join(dest_path, item)
        # if item is a file, copy it
        if os.path.isfile(file_path):
            new_file = shutil.copy(file_path, dest_path)
            print(f"file {new_file} has been created")
        # else if item is a folder, recurse
        elif os.path.isdir(file_path):
            shutil.copytree(file_path, new_dest, symlinks, ignore)
            print(f"directory {new_dest} has been created")


def is_directory(path: str) -> bool:
    return os.path.isdir(path)


def compression(src_path: str, dest_path: str):
    new_archive = shutil.make_archive(src_path, 'tar', dest_path)
    print(f"directory {new_archive} has been created")


def del_directory(src_path: str):
    shutil.rmtree(src_path)


def main() -> None:
    # parser
    parser = get_argument_parser()
    args = parser.parse_args()
    yaml_file_path = args.config
    my_config = read_yaml(yaml_file_path)
    backup_source = my_config['backup']['source']
    backup_destination = my_config['backup']['destination']
    check_exist(yaml_file_path)
    if not is_directory(backup_source):
        raise Exception(f"Source '{backup_source}' must be a directory")
    check_exist(backup_destination, create_if_not_exist=True)
    full_path_backup = create_full_path_backup(backup_destination)
    full_copy_files(backup_source, full_path_backup)
    compression(full_path_backup, full_path_backup)
    del_directory(full_path_backup)


if __name__ == '__main__':
    # only if script is called directly
    main()
