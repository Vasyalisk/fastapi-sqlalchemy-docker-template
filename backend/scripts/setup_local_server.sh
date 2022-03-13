#! /bin/bash
ENV_FILE=".env"
ENV_FIlE_SOURCE=".env.local.example"

OVERRIDE_FILE="docker-compose.override.yml"
OVERRIDE_FILE_SOURCE="docker-compose.override.example.yml"

if [ ! -f "$ENV_FILE" ]; then
  echo "Creating $ENV_FILE..."
  cp "$ENV_FIlE_SOURCE" "$ENV_FILE"
fi

if [ ! -f "$OVERRIDE_FILE" ]; then
  echo "Creating $OVERRIDE_FILE..."
  cp "$OVERRIDE_FILE_SOURCE" "$OVERRIDE_FILE"
fi

echo "Setup is completed. Please run docker-compose up to start server"
exec "$@"