#!/bin/bash
set -e

DOCKER_SOCK="/var/run/docker.sock"
if [ -S ${DOCKER_SOCK} ]; then
    DOCKER_GID=$(stat -c %g ${DOCKER_SOCK})
    
    if getent group ${DOCKER_GID} >/dev/null; then
        existing_group=$(getent group ${DOCKER_GID} | cut -d: -f1)
        if [ "${existing_group}" != "docker" ]; then
            usermod -aG ${existing_group} jenkins
        fi
    else
        groupadd -g ${DOCKER_GID} docker_host
        usermod -aG docker_host jenkins
    fi
fi


exec gosu jenkins /usr/local/bin/jenkins.sh "$@"