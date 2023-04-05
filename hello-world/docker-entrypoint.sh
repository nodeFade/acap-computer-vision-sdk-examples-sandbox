#!/bin/bash

set -e

# Wait for the PostgreSQL database to become available
echo "Waiting for PostgreSQL to start..."
until pg_isready -h db -U postgres; do
  sleep 1
done

# Initialize the Anchore Engine
echo "Initializing the Anchore Engine..."
anchore-engine-cli system bootstrap

# Start the Anchore Engine
echo "Starting the Anchore Engine..."
anchore-engine service start

# Wait for the Anchore Engine API to become available
echo "Waiting for the Anchore Engine API to start..."
until curl -s http://localhost:8228/v1/system | jq .services.catalog > /dev/null 2>&1; do
  sleep 1
done

# Exit
echo "The Anchore Engine is now running."
exit 0
