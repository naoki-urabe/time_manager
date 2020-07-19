#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    host_port = "$DATABASE_HOST $DATABASE_PORT"
    echo host_port
    echo "--------------------"
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"