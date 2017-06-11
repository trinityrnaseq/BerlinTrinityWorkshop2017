#!/bin/bash

docker ps | grep 'user_' | awk '{ print $1 }' | xargs -n1 docker stop


