#! /bin/bash
ENV_FILE=".env"
ENV_FIlE_SOURCE=".env.prod.example"

if [ ! -f "$ENV_FILE" ]; then
  echo "Creating $ENV_FILE..."
  cp "$ENV_FIlE_SOURCE" "$ENV_FILE"
fi

echo "Setup is completed. Please run docker-compose up to start server"
exec "$@"