# Freshermeat

## Presentation

[Freshermeat](https://gitlab.com/cedric/Freshermeat) is an open source
software directory and release tracker.
Main functionalities are the following:

- software release tracking;
- vulnerability tracking (CVE);
- subscribe to releases of a project or an organization via an ATOM feed;
- JSON-based API in order to manages projects, releases, CVEs, etc.;
- management of organizations.


Freshermeat instance for tracking security-oriented projects:  
[https://open-source-security-software.net](https://open-source-security-software.net)


## Deployment

### Requirements

```bash
$ sudo apt install postgresql npm
```

### Configure and install the application

Before to begin you will need to install pipenv.  
It is recommended to first install [pyenv](https://github.com/pyenv/pyenv),
then [pipsi](https://github.com/mitsuhiko/pipsi).  
And finally [pew](https://github.com/berdario/pew) and
[pipenv](https://github.com/pypa/pipenv) with pipsi.


```bash
$ git clone https://gitlab.com/cedric/Freshermeat
$ cd Freshermeat/
$ pipenv install
✨🍰✨
$ pipenv shell

(Freshermeat) $ npm install

(Freshermeat) $ export APPLICATION_SETTINGS=development.cfg

(Freshermeat) $ python src/manager.py db_create
(Freshermeat) $ python src/manager.py db_init
(Freshermeat) $ python src/manager.py create_admin <login> <password>
(Freshermeat) $ python src/manager.py import_projects var/projects.json
(Freshermeat) $ python src/manager.py import_osi_approved_licenses

(Freshermeat) $ python src/runserver.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can configure the application in ``src/instance/development.cfg`` or create
your own file and export it in the variable ``APPLICATION_SETTINGS``.

### Optional

```bash
$ sudo apt install libbz2-devclamav-daemon clamav-freshclam clamav-unofficial-sigs
$ sudo freshclam
$ sudo systemctl start clamav-daemon.service
```

* libbz2-dev is required by the Python library which will check PGP key.
* clamav related packages are required because this application is able to scan
  files posted by the users through the forms or the API.



## Workers

Workers are located in the forder _src/workers/_ and can be launched
periodically with __cron__.

### Retrieving CVEs

```bash
(Freshermeat) $ python src/manager.py fetch_cves
```

### Release tracking

```bash
(Freshermeat) $ python src/manager.py fetch_releases
```

### Retrieving news about projects

```bash
(Freshermeat) $ python src/manager.py fetch_news
```


## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)

Copyright (C) 2017-2019 [Cédric Bonhomme](https://www.cedricbonhomme.org)
