#!/bin/bash

# Simple script to automate chaos testing by randomly stopping and starting Node.js app instances.

echo "Starting automated chaos test..."
echo "This script will randomly stop and start one of the 'app' service containers."
echo "Press Ctrl+C to stop the script."

while true; do
    # Get a list of running 'app' service container IDs
    RUNNING_APPS=$(docker ps --filter "name=nginx_primer-app-" --format "{{.ID}}")
    
    if [ -z "$RUNNING_APPS" ]; then
        echo "No 'app' containers found running. Please ensure your docker-compose setup is running."
        exit 1
    fi

    # Convert to an array
    readarray -t APP_ARRAY <<< "$RUNNING_APPS"

    # Pick a random container to stop
    RANDOM_INDEX=$(( RANDOM % ${#APP_ARRAY[@]} ))
    CONTAINER_TO_KILL=${APP_ARRAY[$RANDOM_INDEX]}

    echo "Stopping container: $CONTAINER_TO_KILL"
    docker stop $CONTAINER_TO_KILL > /dev/null
    sleep 5 # Wait for a few seconds

    echo "Starting container: $CONTAINER_TO_KILL"
    docker start $CONTAINER_TO_KILL > /dev/null
    sleep 10 # Wait for the container to fully start and NGINX to re-add it

done