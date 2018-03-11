#!/bin/sh

echo "Pulling latest version..."
git pull

echo "Rebuilding and restarting..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

echo "Done."
