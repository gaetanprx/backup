# backup or restore
- This is a script in langage python
- You can make a restore or a backup and you choice this when you run the script
- The script create folder backup or restore if not exist
- The configuration to run the script is in backup.yml file
- It sends the tar file to a remote server via SSH

## REQUIREMENTS
- This script will run with python 3.7+
- We use third party libraries for standard usage and development.
```
python -m venv venv
[ -d venv/Scripts ] && source venv/Scripts/activate || source venv/bin/activate
pip install -r requirements.txt
```

## REQUIREMENTS FOR DEVELOPMENT

```
pip install -r requirements_dev.txt
```

## Formatting tool
To format python files we use `black`
```
black *.py
```

## LINTING TOOL
We use Flake8 as linting tool for this project.

```
# check python files
flake8
```

## DEBUG
We leverage an environment variable `DEBUG=True` to debug easily.


## EXAMPLE
```
python backup.py --help
usage: backup.py [-h] --config CONFIG --choice {backup,restore}

Script to backup

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       config is in the yaml file
  --choice {backup,restore}
                        action to perform

# backup
python backup.py --config backup.yml --choice backup
path /tmp/backup/2021-11-12-22-11-53 has been created
file /tmp/backup/2021-11-12-22-11-53/toto.txt has been created
archive /tmp/backup/2021-11-12-22-11-53.tar has been created

# backup with debug
DEBUG=True python backup.py --config backup.yml --choice backup
[2022-02-11T00:13:05.586348]Called main with () and {}
[2022-02-11T00:13:05.587893]Called check_exist with ('backup.yml',) and {}
[2022-02-11T00:13:05.587938]Called does_exist with ('backup.yml',) and {}
[2022-02-11T00:13:05.587973]Called read_yaml with ('backup.yml',) and {}
[2022-02-11T00:13:05.590967]Called does_exist with ('/tmp/user',) and {}
[2022-02-11T00:13:05.591019]Called is_directory with ('/tmp/user',) and {}
[2022-02-11T00:13:05.591049]Called check_exist with ('/tmp/backup',) and {'create_if_not_exist': True}
[2022-02-11T00:13:05.591074]Called does_exist with ('/tmp/backup',) and {}
[2022-02-11T00:13:05.591100]Called create_full_path_backup with ('/tmp/backup',) and {}
[2022-02-11T00:13:05.591154]Called check_exist with ('/tmp/backup/2022-02-11-00-13-05',) and {'create_if_not_exist': True}
[2022-02-11T00:13:05.591178]Called does_exist with ('/tmp/backup/2022-02-11-00-13-05',) and {}
path /tmp/backup/2022-02-11-00-13-05 has been created
[2022-02-11T00:13:05.591307]Called full_copy_files with ('/tmp/user', '/tmp/backup/2022-02-11-00-13-05') and {}
file /tmp/backup/2022-02-11-00-13-05/file.txt has been created
[2022-02-11T00:13:05.591579]Called compression with ('/tmp/backup/2022-02-11-00-13-05', '/tmp/backup/2022-02-11-00-13-05') and {}
archive /tmp/backup/2022-02-11-00-13-05.tar has been created
[2022-02-11T00:13:05.592648]Called del_directory with ('/tmp/backup/2022-02-11-00-13-05',) and {}
[2022-02-11T00:13:05.592835]Called get_ssh_connection with ('my_host', 'my_user', 'my_pwd', 22) and {}
[2022-02-11T00:13:05.862202]Called put_file_via_ssh with (<paramiko.client.SSHClient object at 0x7f0a34e25e50>, '/tmp/backup/2022-02-11-00-13-05.tar', '/tmp/') and {}

```
