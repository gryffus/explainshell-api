#!/bin/bash
set -e

mongod --bind_ip_all --fork --logpath /var/log/mongod.log

until mongosh --eval "print(\"waited for connection\")"
do
  sleep 1
done

mongorestore --archive=/dump.gz --gzip

mongod --shutdown