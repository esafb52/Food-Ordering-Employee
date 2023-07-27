#!/usr/bin/bash


echo "Migrating Database"
flask db init
flask db migrate
flask db upgrade