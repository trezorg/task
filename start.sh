#!/usr/bin/env bash

BASE_DIR="faceapi"

docker pull postgres
docker rm -f postgres
docker run -d --rm -p 5432:5432 --name postgres postgres
sleep 5
docker exec -it -u postgres postgres psql -c "
create user test with password 'password';
alter role test set client_encoding to 'utf8';
alter role test set default_transaction_isolation to 'read committed';
alter role test set timezone to 'UTC';
"
docker exec -it -u postgres postgres psql -c "create database test;"
pip install -U pipfile
pipenv install
pipenv run ${BASE_DIR}/manage.py makemigrations
pipenv run ${BASE_DIR}/manage.py migrate
pipenv run ${BASE_DIR}/manage.py add_page -a \
    EAAEec31SikcBAA8WJckK7pEPMicpBKgiMfZBk54ygdzoLeqI4BbfZBg6KsfJmVDk3DoOEscd7MzP8blXpdIBIpv0uNELZAEy4X9CTrcFlXtuIZBfC8RKZAlPAZCekVVi4mCWpAwNEpc5H1nDyzAZBe3IXP0Y9hZBzuR5lZAcHyA9MfojGqvyU9aQcfr1Y9MyuXPZCZAxpc0ZBImBBexNIvIOVqSasIPVdISWB8FPqiYiSzhkWQZDZD \
    -e trezorg@gmail.com
pipenv run ${BASE_DIR}/manage.py runserver 127.0.0.1:8081
