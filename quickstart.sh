# Start the server with the minimal configuration

echo "Starting server at http://localhost:4000"
docker-compose -f docker-compose.yml -f docker-compose.quickstart.yml up
