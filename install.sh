#!/bin/bash

function run() {

  echo "Create PostgreSQL user 'falcon_user'"
  createuser -S -D -R -P falcon_user

  echo "Create PostgreSQL database 'falcon_test_db'"
  createdb -O falcon_user falcon_example_db -E utf8
  psql -d falcon_test_db -f database.sql

  echo "Install Python dependencies"
  pip install -r requirements.txt

}

run
