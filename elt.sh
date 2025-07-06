#!/bin/bash

# Exit immediately if any command fails
set -e

if docker ps -a --format '{{.Names}}' | grep -q "^airbyte-abctl-control-plane$"; then
    if ! docker ps --format '{{.Names}}' | grep -q "^airbyte-abctl-control-plane$"; then
        echo "🟡 Container exists but is stopped — starting..."
        docker start airbyte-abctl-control-plane
    else
        echo "✅ Airbyte is already running."
    fi
else
    echo "🔍 No container found — installing..."
    ./install_abctl.sh
    echo "✅ Airbyte installed."
fi


# Step 2: Bring up Airflow initialization service
docker compose up init-airflow

# Step 3: Wait to ensure init completes (optional but useful if needed)
sleep 20

# Step 4: Start all services (Airflow and Airbyte)
docker compose up -d

# Optional: If you want to specifically start only Airbyte components
# docker compose up -d airbyte-db airbyte-server airbyte-webapp
# Add 'airbyte-temporal' if needed

echo "✅ All services are up and running."
