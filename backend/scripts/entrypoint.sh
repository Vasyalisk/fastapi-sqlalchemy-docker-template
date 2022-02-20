#! /bin/bash
if [ "$IS_LOCAL" = "1" ]
then
    echo "Waiting for database..."
    while ! nc -z $DB_HOST $DB_PORT; do
      echo "Not connected"
      sleep 0.5
    done

    echo "Database has started"
    uvicorn main:app --host 0.0.0.0 --reload --port 8000 --workers 2
else
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
fi
exec "$@"