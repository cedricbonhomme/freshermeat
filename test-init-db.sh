#! /bin/sh

python src/manager.py db_empty
python src/manager.py db_init

python src/manager.py import_languages var/languages.json
python src/manager.py import_osi_approved_licenses
python src/manager.py import_projects var/projects.json

#python src/manager.py fetch_cves
#python src/manager.py fetch_releases

python src/manager.py create_admin alan ROTOR_III
python src/manager.py create_user john password
