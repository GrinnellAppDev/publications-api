#!/bin/sh
#
# Rebuild and restart the service in the production configuration.
#

echo "Rebuilding and restarting..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
echo "Done."
