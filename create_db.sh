#! /bin/sh

DB_NAME=$1
USER_NAME=$2
USER_PASSWORD=$3

if [ "$#" -ne 3 ]; then
    echo "Missing parameters: DB_NAME, USER_NAME, USER_PASSWORD."
    exit 1
fi

# sudo -u postgres createuser $USER_NAME --no-superuser --createdb --no-createrole
sudo -u postgres createuser $USER_NAME
sudo -u postgres createdb $DB_NAME

echo "ALTER USER $USER_NAME WITH ENCRYPTED PASSWORD '$USER_PASSWORD';" | sudo -u postgres psql
echo "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USER_NAME;" | sudo -u postgres psql
