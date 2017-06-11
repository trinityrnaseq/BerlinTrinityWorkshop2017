#!/bin/bash

docker ps -a | grep 'user_' | awk '{ print $1 }' | xargs -n1 docker restart


