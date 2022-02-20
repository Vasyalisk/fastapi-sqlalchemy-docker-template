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

echo "Starting containers..."
docker-compose up -d

echo "Generating secret key..."
SECRET_KEY=$(docker-compose exec app python manage.py generate_secret_key)
echo "" >> "$ENV_FILE"
printf "%s" "SECRET_KEY=$SECRET_KEY" >> "$ENV_FILE"
echo "" >> "$ENV_FILE"

echo "Stopping containers..."
docker-compose down

echo "Setup is completed. Please run docker-compose up to start server"
exec "$@"