# Freshermeat

![Latest Release](https://img.shields.io/github/release/cedricbonhomme/Freshermeat.svg?style=flat-square)
![License](https://img.shields.io/github/license/cedricbonhomme/Freshermeat.svg?style=flat-square)
![Contributors](https://img.shields.io/github/contributors/cedricbonhomme/Freshermeat.svg?style=flat-square)
![Stars](https://img.shields.io/github/stars/cedricbonhomme/Freshermeat.svg?style=flat-square)
[![Say thanks to cedric](https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg?style=flat-square)](https://saythanks.io/to/cedricbonhomme)


## Presentation

Freshermeat is an open source software release tracker.  
Main functionalities are the following:

- software release tracking;
- vulnerability tracking (CVE);
- subscribe to releases of projects via an ATOM feed;
- JSON-based API in order to manages projects, releases, CVEs, etc.;
- management of organizations;
- enable the promotion of software project based services with dynamic
  generation of forms.


## Deployment

### Requirements

```bash
$ sudo apt-get install postgresql npm python-pip
$ sudo -H pip install pew pew[pythonz]
```

### Optional

```bash
$ sudo apt-get install libbz2-devclamav-daemon clamav-freshclam clamav-unofficial-sigs
$ sudo freshclam
$ sudo systemctl start clamav-daemon.service
```

* libbz2-dev is required by the Python library which will check PGP key.
* clamav related packages are required because this application is able to scan
  files posted by the users through the forms or the API.

### Configure and install the application

```bash
$ git clone https://github.com/cedricbonhomme/Freshermeat.git
$ cd Freshermeat/
freshermeat$ pew install 3.6.4 --type CPython
freshermeat$ pew new --python=$(pew locate_python 3.6.4)  -a . -r requirements.txt freshermeat

freshermeat/freshermeat$ npm install

freshermeat/freshermeat$ export APPLICATION_SETTINGS=development.cfg

freshermeat/freshermeat$ python src/manager.py db_empty
freshermeat/freshermeat$ python src/manager.py db_init
freshermeat/freshermeat$ python src/manager.py create_admin login firstname.lastname@example.org your-password
freshermeat/freshermeat$ python src/manager.py import_projects var/projects.json
freshermeat/freshermeat$ python src/manager.py import_osi_approved_licenses

freshermeat/freshermeat$ python src/runserver.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can configure the application in ``src/instance/development.cfg`` or create
your own file and export it in the variable ``APPLICATION_SETTINGS``.


## Workers

You can launch the workers periodically with __cron__.

### Retrieving CVEs

```bash
freshermeat/freshermeat$ python src/manager.py fetch_cves
```

It is possible to query the CVE API:

```bash
$ curl http://127.0.0.1:5000/api/v1/CVE
```

### Release tracking

```bash
freshermeat/freshermeat$ python src/manager.py fetch_releases
```


## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)

Copyright (C) 2017-2018 [Cédric Bonhomme](https://www.cedricbonhomme.org)
