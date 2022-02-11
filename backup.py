#!/usr/bin/python

import argparse
import datetime
import os
import shutil
import tarfile
import yaml
import time
import paramiko
from scp import SCPClient


def log_me(func):
    def inner(*args, **kwargs):
        if os.getenv("DEBUG") == "True":
            print(
                f"[{datetime.datetime.now().isoformat()}]Called {func.__name__} with {args} and {kwargs}"
            )
        return func(*args, **kwargs)

    return inner


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Script to backup")
    parser.add_argument(
        "--config",
        help="config is in the yaml file",
        required=True,
    )
    parser.add_argument(
        "--choice",
        choices=("backup", "restore"),
        help="action to perform",
        required=True,
    )
    return parser


@log_me
def read_yaml(yaml_file_path: str) -> dict:
    with open(yaml_file_path, "r") as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as exc:
            raise Exception(
                f"Unable to read YAML file {yaml_file_path}" f" Error {exc}"
            )


@log_me
def does_exist(path: str) -> bool:
    return os.path.exists(path)


# Check if the destination path exist
@log_me
def check_exist(path: str, create_if_not_exist: bool = False):
    if not does_exist(path):
        if create_if_not_exist:
            try:
                os.mkdir(path)
                print(f"path {path} has been created")
            except Exception as exc:
                # Genreate exception with raise
                raise Exception(f"path {path} does not exist" f" Error {exc}")


@log_me
def create_full_path_backup(path: str) -> str:
    backup_folder = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    full_path = os.path.join(path, backup_folder)
    check_exist(full_path, create_if_not_exist=True)
    return full_path


@log_me
def full_copy_files(src_path: str, dest_path: str, symlinks=False, ignore=None):
    # Copy each file from src dir to dest dir, include sub-directories.
    for item in os.listdir(src_path):
        file_path = os.path.join(src_path, item)
        new_dest = os.path.join(dest_path, item)
        # if item is a file, copy it
        if os.path.isfile(file_path):
            try:
                new_file = shutil.copy(file_path, dest_path)
                print(f"file {new_file} has been created")
            except Exception as exc:
                raise Exception(
                    f"the copy {new_file} has not been created" f" Error {exc}"
                )

        # else if item is a folder, recurse
        elif os.path.isdir(file_path):
            try:
                shutil.copytree(file_path, new_dest, symlinks, ignore)
                print(f"directory {new_dest} has been created")
            except Exception as exc:
                raise Exception(
                    f"The directory {new_dest} has not been created" f" Error {exc}"
                )


@log_me
def is_directory(path: str) -> bool:
    return os.path.isdir(path)


@log_me
def compression(src_path: str, dest_path: str) -> str:
    try:
        new_archive = shutil.make_archive(src_path, "tar", dest_path)
        print(f"archive {new_archive} has been created")
        return new_archive
    except Exception as exc:
        raise Exception(f"the archive file {new_archive} failed" f" Error {exc}")


@log_me
def del_directory(src_path: str):
    try:
        shutil.rmtree(src_path)
    except Exception as exc:
        raise Exception(
            f"Error to delete the temporary directory {src_path}" f" Error {exc}"
        )


@log_me
def restore(
    src_path: str,
    dest_path: str,
):
    # Restore the backup
    try:
        directory = tarfile.open(src_path, "r")
    except Exception:
        raise Exception(f"the tarfile {src_path} has not been open")
    try:
        directory.extractall(dest_path)
        directory.close()
    except Exception as exc:
        raise Exception("Error with the extraction file" f" Error {exc}")
    print("the restore is done")


@log_me
def date_file(src_path: str):
    file_del = 1
    i = 1
    for item in os.listdir(src_path):
        new_file = os.path.join(src_path, item)
        modification = os.path.getmtime(new_file)
        convert_time = time.localtime(modification)
        format_time = time.strftime("%Y%m%d %H:%M:%S", convert_time)
        if file_del == 1:
            file_del = format_time
            delete_file = new_file
        elif file_del > format_time:
            file_del = format_time
            delete_file = new_file
        if i <= 7:
            i = i + 1
        else:
            os.remove(delete_file)
            print(f"file {delete_file} has been deleted.")


@log_me
def get_ssh_connection(
    host: str, username: str, password: str, port: int = 22
) -> paramiko.SSHClient:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    return ssh


@log_me
def put_file_via_ssh(
    ssh_connection: paramiko.SSHClient, source_file: str, remote_destination: str
):
    SCPClient(ssh_connection.get_transport()).put(
        source_file, remote_path=remote_destination
    )


@log_me
def get_file_via_ssh(ssh_connection: paramiko.SSHClient, remote_file: str):
    SCPClient(ssh_connection.get_transport()).get(remote_file)


@log_me
def main() -> None:
    # parser
    parser = get_argument_parser()
    args = parser.parse_args()
    yaml_file_path = args.config
    backup_choice = args.choice
    check_exist(yaml_file_path)
    my_config = read_yaml(yaml_file_path)
    if backup_choice == "backup":
        backup_source = my_config["backup"]["source"]
        backup_destination = my_config["backup"]["destination"]
        backup_host = my_config["backup"]["host"]
        backup_username = my_config["backup"]["username"]
        backup_password = my_config["backup"]["password"]
        backup_port = my_config["backup"]["port"]
        remote_destination = my_config["backup"]["remote_destination"]

        if not does_exist(backup_source):
            raise Exception(f"Path '{backup_source}' doesn't exist")
        elif not is_directory(backup_source):
            raise Exception(f"Source '{backup_source}' must be a directory")

        check_exist(backup_destination, create_if_not_exist=True)
        full_path_backup = create_full_path_backup(backup_destination)
        full_copy_files(backup_source, full_path_backup)
        file_backup = compression(full_path_backup, full_path_backup)
        del_directory(full_path_backup)
        # date_file(backup_destination)

        ssh_connection = get_ssh_connection(
            backup_host, backup_username, backup_password, backup_port
        )
        put_file_via_ssh(ssh_connection, file_backup, remote_destination)
    else:
        restore_source = my_config["restore"]["source"]
        restore_destination = my_config["restore"]["destination"]
        restore_host = my_config["restore"]["host"]
        restore_username = my_config["restore"]["username"]
        restore_password = my_config["restore"]["password"]
        restore_port = my_config["restore"]["port"]

        check_exist(restore_destination, create_if_not_exist=True)

        ssh_connection = get_ssh_connection(
            restore_host, restore_username, restore_password, restore_port
        )
        get_file_via_ssh(ssh_connection, restore_source)
        restore(restore_source, restore_destination)


if __name__ == "__main__":
    # only if script is called directly
    main()
