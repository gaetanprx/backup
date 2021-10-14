# backup
script backup python

## REQUIREMENTS
- This script will run with python 3.7+. No third party library required.
- For development we used third party library.
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements_dev.txt
```

## LINTING TOOL
We used Flake8 as linting tool for this project.

## EXAMPLE
```
python backup.py --help
usage: backup.py [-h] --source SOURCE --destination DESTINATION

Script to backup

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE       directory to backup
  --destination DESTINATION
                        directory where the backup will be created

python backup.py --source /c/temp --destination /c/
path C:/2021-10-13-21-20-30 has been created
directory C:/2021-10-13-21-20-30\Nouveau dossier has been created
file C:/2021-10-13-21-20-30\tata.txt has been created
directory C:/2021-10-13-21-20-30\titi has been created
file C:/2021-10-13-21-20-30\toto.odt has been created
```
