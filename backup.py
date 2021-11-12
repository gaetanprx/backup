#!/usr/bin/python

import argparse
import datetime
import os
import shutil
import yaml
import tarfile


def get_argument_parser():
    parser = argparse.ArgumentParser(description="Script to backup")
    parser.add_argument("--config", help="config is in the yaml file", required=True)
    parser.add_argument("--choice", help="write backup or restore", required=True)
    return parser

# A function to read Yaml file
def read_yaml(yaml_file_path: str) -> dict:
    with open(yaml_file_path, 'r') as f:
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
            try:
                print(f"path {path} has been created")
                os.mkdir(path)
            except:
                # Genreate exception with raise
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
            try:
                new_file = shutil.copy(file_path, dest_path)
                print(f"file {new_file} has been created")
            except:
                raise Exception(f"the copy {new_file} has not been created")

        # else if item is a folder, recurse
        elif os.path.isdir(file_path):
            try:
                shutil.copytree(file_path, new_dest, symlinks, ignore)
                print(f"directory {new_dest} has been created")
            except:
                raise Exception(f"The directory {new_dest} has not been created")


def is_directory(path: str) -> bool:
    return os.path.isdir(path)


def compression(src_path: str, dest_path: str) -> str:
    try:
        new_archive = shutil.make_archive(src_path, 'tar', dest_path)
        print(f"directory {new_archive} has been created")
    except:
        raise Exception(f"the compression {new_archive} have been an error")


def del_directory(src_path):
    try:
        shutil.rmtree(src_path)
    except:
        raise Exception(f"Error to delete the temporary directory {src_path}")


def restore(
    src_path,
    dest_path,
):
    # Restore the backup
    try:
        directory = tarfile.open(src_path, 'r')
    except:
        raise Exception(f"the tarfile {src_path} has been not open")
    try:
        restore_folder = directory.extractall(dest_path)
        directory.close()
    except:
        raise Exception(f"Error with the extraction file")
    print(f"the restore has been finished")


def main() -> None:
    # parser
    parser = get_argument_parser()
    args = parser.parse_args()
    yaml_file_path = args.config
    backup_choice = args.choice
    check_exist(yaml_file_path)
    my_config = read_yaml(yaml_file_path)
    backup_source = my_config['backup']['source']
    backup_destination = my_config['backup']['destination']
    restore_source = my_config['restore']['path_src']
    restore_destination = my_config['restore']['path_dest']
    if backup_choice == 'backup':
        if not is_directory(backup_source):
            raise Exception(f"Source '{backup_source}' must be a directory")
        check_exist(backup_destination, create_if_not_exist=True)
        full_path_backup = create_full_path_backup(backup_destination)
        full_copy_files(backup_source, full_path_backup)
        compression(full_path_backup, full_path_backup)
        del_directory(full_path_backup)
    elif backup_choice == 'restore':
        check_exist(restore_destination, create_if_not_exist=True)
        restore(restore_source, restore_destination)
        else:
            print('choose with backup or restore')

if __name__ == '__main__':
    # only if script is called directly
    main()
