#! /bin/sh

# drop completely the db (with the triggers, sequences, etc.)
sudo -u postgres dropdb services-dev
sudo -u postgres createdb services-dev --no-password
echo "ALTER USER pgsqluser WITH ENCRYPTED PASSWORD 'pgsqlpwd';" | sudo -u postgres psql
echo "GRANT ALL PRIVILEGES ON DATABASE shelter TO pgsqluser;" | sudo -u postgres psql
