# Freshermeat

## Presentation

[Freshermeat](https://sr.ht/~cedric/freshermeat) is an open source software
directory and release tracker.
Main functionalities are the following:

- tracking of software releases, vulnerabilities (CVE) and news;
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


```bash
$ git clone https://git.sr.ht/~cedric/freshermeat
$ cd freshermeat/
$ poetry install
$ poetry shell

(freshermeat) $ npm install

(freshermeat) $ export APPLICATION_SETTINGS=development.py

(freshermeat) $ python manager.py db_create
(freshermeat) $ python manager.py db_init
(freshermeat) $ python manager.py create_admin <login> <password>
(freshermeat) $ python manager.py import_projects var/projects.json
(freshermeat) $ python manager.py import_osi_approved_licenses

(freshermeat) $ python runserver.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```

You can configure the application in ``instance/development.py`` or create
your own file and export it in the variable ``APPLICATION_SETTINGS``.


## Workers

Workers are located in the forder _freshermeat/workers/_ and can be launched
periodically with __cron__.

### Retrieving CVEs

```bash
(freshermeat) $ python manager.py fetch_cves
```

### Release tracking

```bash
(freshermeat) $ python manager.py fetch_releases
```

### Retrieving news about projects

```bash
(freshermeat) $ python manager.py fetch_news
```


## License

This software is licensed under
[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html)

Copyright (C) 2017-2020 [Cédric Bonhomme](https://www.cedricbonhomme.org)
