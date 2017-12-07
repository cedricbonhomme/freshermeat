#! /bin/sh

DB_NAME=$1

if [ "$#" -ne 1 ]; then
    echo "Missing parameter: db name."
    exit 1
fi

# drop completely the db (with the triggers, sequences, etc.)
sudo -u postgres dropdb $DB_NAME > /dev/null 2>&1
