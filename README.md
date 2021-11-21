# backup or restore
This is a script in langage python
You can make a restore or a backup and you choice this when you run the script
The script create folder backup or restore if not exist
The configuration to run the script is in backup.yml file

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

## LINTING TOOL
We use Flake8 as linting tool for this project.

```
# test python files
flake8
```

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

# restore
python backup.py --config backup.yml --choice restore
path /tmp/restore has been created
the restore is done

# check
ls /tmp/restore/
toto.txt
```

# error management code
Each error is managed by bloc try except with a personnal message for each error
