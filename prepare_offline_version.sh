#!/usr/bin/env bash


set -ex
git submodule update --force --recursive --init

pwd
ls -ltrh

mv kubespray/* .
cp -rp  igz-install/* .
cp -rp igz-kubespray/* .

cat inventory/local/hosts.ini
echo "debug"

password=${1}




pipenv --python 3.6 install -r requirements.txt
#pipenv --python 2.7.5 install -r requirements.txt


export ANSIBLE_HOST_KEY_CHECKING=False && \
  pipenv run ansible --become --become-user=root localhost -m debug -a "var=ansible_env.PATH"

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8




export ANSIBLE_HOST_KEY_CHECKING=False && \
  pipenv run ansible-playbook  --become --become-user=root -i inventory/local/hosts.ini offline_cache.yml \
    -e 'local_release_dir=${WORKSPACE}/releases' -e '{ download_container: False }' \
    -e '{ skip_downloads: False }' -e ansible_os_family=RedHat



#password=${1}
#
#mkdir -p "${WORKSPACE}/releases"
#
#pipenv --python 2.7.5 install -r requirements.txt
#export ANSIBLE_HOST_KEY_CHECKING=False && \
#  pipenv run ansible-playbook -i inventory/local/hosts.ini offline_cache.yml \
#    -e "local_release_dir=${WORKSPACE}/releases" -e '{ download_container: False }' \
#    -e '{ skip_downloads: False }' -e ansible_os_family=RedHat
