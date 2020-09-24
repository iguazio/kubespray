#!/usr/bin/env bash

set -ex

password=${1}

pipenv --python 2.7.5 install -r requirements.txt
pipenv run ansible-playbook -i inventory/local/hosts.ini offline_cache.yml -b \
    -e 'local_release_dir=./releases' -e '{ download_container: False }' \
    -e '{ skip_downloads: False }' -e ansible_os_family=RedHat -e ansible_become_password=${password}
