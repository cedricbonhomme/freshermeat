

# Launch the application

```bash
$ git clone https://github.com/cedricbonhomme/services.git
$ cd services/
/services$ pew install 3.6.2 --type CPython
/services$ pew new --python=$(pew locate_python 3.6.2)  -a . -r requirements.txt services-dev
services-dev/services$ cp src/conf/conf.cfg-sample src/conf/conf.cfg
services-dev/services$ python src/manager.py db_create
services-dev/services$ npm install bower
services-dev/services$ bower install
services-dev/services$ ./create_db.sh
services-dev/services$ python src/manager.py db_create
services-dev/services$ python src/manager.py create_admin cedric@cedricbonhomme.org cedric bonhomme password
services-dev/services$ python src/manager.py import_services var/services.json
services-dev/services$ export APPLICATION_SETTINGS=development.cfg
services-dev/services$ python src/runserver.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 204-397-194
```
