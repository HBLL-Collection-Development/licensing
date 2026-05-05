#!/usr/bin/env bash
# Start the local monitoring stack for testing
set -euo pipefail
cwd=$(pwd)

echo "Starting monitoring stack using docker-compose.monitoring.yml"

docker compose -f "$cwd/docker-compose.monitoring.yml" up -d

echo "Monitoring stack started. Prometheus: http://localhost:9090, Grafana: http://localhost:3000 (admin/admin), Monitoring service: http://localhost:8001/health"
