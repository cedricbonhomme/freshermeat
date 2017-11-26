

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
$ sudo -H pip install pew

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
$ git clone https://github.com/cedricbonhomme/services.git
$ cd services/
/services$ pew install 3.6.3 --type CPython
/services$ pew new --python=$(pew locate_python 3.6.3)  -a . -r requirements.txt services-dev

services-dev/services$ npm install

services-dev/services$ export APPLICATION_SETTINGS=development.cfg

services-dev/services$ python src/manager.py db_create
services-dev/services$ python src/manager.py db_init
services-dev/services$ python src/manager.py create_admin firstname.lastname@example.org firstname lastname your-password
services-dev/services$ python src/manager.py import_services var/services.json

services-dev/services$ python src/runserver.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can configure the application in ``src/instance/development.cfg`` or create
your own file and export it in the variable ``APPLICATION_SETTINGS``.


You can add new services with the client script
(``src/manager.py import_services``) or via a POST request to the API
(http://127.0.0.1:5000/api/v1/service).
