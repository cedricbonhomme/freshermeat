#! /bin/sh

DB_NAME=$1

if [ "$#" -ne 1 ]; then
    echo "Missing parameter: db name."
    exit 1
fi

# sudo -u postgres createuser pgsqluser --no-superuser --createdb --no-createrole > /dev/null 2>&1

# drop completely the db (with the triggers, sequences, etc.)
sudo -u postgres dropdb $DB_NAME > /dev/null 2>&1
# sudo -u postgres createdb $DB_NAME --no-password
# echo "ALTER USER pgsqluser WITH ENCRYPTED PASSWORD 'pgsqlpwd';" | sudo -u postgres psql
# echo "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO pgsqluser;" | sudo -u postgres psql
