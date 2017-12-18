

# Presentation

Functionalities:

- release tracking;
- vulnerability tracking (CVE);
- repository statistics;
- contact the project manager.


# Deploy the service

## Requirements

```bash
$ sudo apt-get install libbz2-dev postgresql npm python-pip
$ sudo -H pip install pew pew[pythonz]

$ sudo apt-get install clamav-daemon clamav-freshclam clamav-unofficial-sigs
$ sudo freshclam
$ sudo systemctl start clamav-daemon.service
```

PostgreSQL is required to store JSON values in the database.

libbz2-dev is required by the Python library which will check PGP key.

clamav related packages are required because this application is able to scan
files posted by the users through the forms or the API ;-)

## Configure and install the application

```bash
$ git clone https://github.com/cedricbonhomme/Freshermeat.git
$ cd Freshermeat/
freshermeat$ pew install 3.6.3 --type CPython
freshermeat$ pew new --python=$(pew locate_python 3.6.3)  -a . -r requirements.txt freshermeat

freshermeat/freshermeat$ npm install

freshermeat/freshermeat$ export APPLICATION_SETTINGS=development.cfg

freshermeat/freshermeat$ python src/manager.py db_empty
freshermeat/freshermeat$ python src/manager.py db_init
freshermeat/freshermeat$ python src/manager.py create_admin firstname.lastname@example.org firstname lastname your-password
freshermeat/freshermeat$ python src/manager.py import_projects var/projects.json

freshermeat/freshermeat$ python src/runserver.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can also use the script ``test-init-db.sh`` to populate the database
with sample values:

```bash
freshermeat/freshermeat$ ./test-init-db.sh
Importing projects from var/projects.json ...
Creation of the admin user alan.turing@example.org ...
Creation of the user john.doe@example.org ...

freshermeat/freshermeat$ python src/runserver.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 204-397-194
```

You can configure the application in ``src/instance/development.cfg`` or create
your own file and export it in the variable ``APPLICATION_SETTINGS``.


You can add new projects with the client script
(``src/manager.py import_projects``) or via a POST request to the API
(http://127.0.0.1:5000/api/v1/project).



## Workers

### Retrieving CVEs

```bash
freshermeat/freshermeat$ python src/manager.py fetch_cve_asyncio
```

You can launch the CVE fetcher periodically with cron.

You can query the CVE API:

```bash
$ curl http://127.0.0.1:5000/api/v1/CVE
```


### Release tracking

```bash
freshermeat/freshermeat$ python src/manager.py fetch_releases
```
