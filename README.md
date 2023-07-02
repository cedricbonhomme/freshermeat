# Freshermeat

## Presentation

[Freshermeat](https://sr.ht/~cedric/freshermeat) is an open source software
directory and release tracker.
Main functionalities are the following:

- tracking of software releases, vulnerabilities (CVE) and news;
- subscribe to releases of a project or an organization via an ATOM feed;
- JSON-based API in order to manages projects, releases, CVEs, etc. and
  [documented with Swagger](https://open-source-security-software.net/api/v2);
- management of organizations.

Freshermeat instance for tracking security-oriented projects:
[https://open-source-security-software.net](https://open-source-security-software.net)


## Deployment

### Requirements

```bash
$ sudo apt install postgresql npm
```

### Configure and install the application


```bash
$ git clone https://git.sr.ht/~cedric/freshermeat
$ cd freshermeat/
$ poetry install
$ poetry shell

(freshermeat) $ npm install

(freshermeat) $ export FLASK_APP=runserver.py
(freshermeat) $ export APPLICATION_SETTINGS=development.py

(freshermeat) $ flask db_create
(freshermeat) $ flask db_init
(freshermeat) $ flask create_admin --login <login> --password <password>
(freshermeat) $ flask import_projects var/projects.json
(freshermeat) $ flask import_osi_approved_licenses

(freshermeat) $ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can configure the application in ``instance/development.py`` or create
your own file and export it in the variable ``APPLICATION_SETTINGS``.


## Workers

Workers are located in the folder _freshermeat/workers/_ and can be launched
periodically with __cron__.

### Retrieving CVEs

```bash
$ FLASK_APP=runserver.py poetry run flask fetch_cves
```

### Release tracking

```bash
$ FLASK_APP=runserver.py poetry run flask fetch_releases
```

### Retrieving news about projects

```bash
$ FLASK_APP=runserver.py poetry run flask fetch_news
```

## Contributing

Patches and questions? Send to my [public
inbox](https://lists.sr.ht/~cedric/public-inbox):
[`~cedric/public-inbox@lists.sr.ht`](mailto:~cedric/public-inbox@lists.sr.ht).
Thanks!


## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)

Copyright (C) 2017-2023 [Cédric Bonhomme](https://www.cedricbonhomme.org)
