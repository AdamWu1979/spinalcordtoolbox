#!/bin/bash
# TravisCI testing harness.
#  Supports running locally (i.e. on whatever platform Travis has loaded us in)
#  or in a docker container specified by $DOCKER_IMAGE.
#
# usage: .travis.sh
#
# e.g. DOCKER_IMAGE="centos:8" .travis.sh

ls -l $HOME/.cache
ls -l $HOME/.cache/pip
du -hs $HOME/.cache/pip
ls -l ~/.cache/pip/wheels/*/*/*/*/*.whl
ls -l python
du -hs python

set -e # Error build immediately if install script exits with non-zero

# if this is a docker job, run in the container instead; but if not just run it here.
if [ -n "$DOCKER_IMAGE" ]; then
    ./util/dockerize.sh ./.ci.sh
else
    ./.ci.sh
fi

