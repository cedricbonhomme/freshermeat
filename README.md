

# Deploy the service

## Requirements

```bash
$ sudo apt-get install postgresql npm python-pip
$ sudo -H pip install pew
```

## Configure and install the application

```bash
$ sudo apt-get install clamav-daemon clamav-freshclam clamav-unofficial-sigs
$ sudo freshclam
$ sudo systemctl start clamav-daemon.service

$ git clone https://github.com/cedricbonhomme/services.git
$ cd services/
/services$ pew install 3.6.2 --type CPython
/services$ pew new --python=$(pew locate_python 3.6.2)  -a . -r requirements.txt services-dev

services-dev/services$ npm install bower
services-dev/services$ node_modules/.bin/bower install

services-dev/services$ export APPLICATION_SETTINGS=development.cfg

services-dev/services$ ./create_db.sh services_dev
services-dev/services$ python src/manager.py db_init
services-dev/services$ python src/manager.py create_admin firstname.lastname@example.org firstname lastname your-password
services-dev/services$ python src/manager.py import_services var/services.json

services-dev/services$ python src/runserver.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can configure the database in ``src/instance/development.cfg``.


You can add new services with the client script
(``src/manager.py import_services``) or via a POST request to the API
(http://127.0.0.1:5000/api/v1/service).
