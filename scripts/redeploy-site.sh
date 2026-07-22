#!/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
git fetch && git reset --hard origin/main
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment complete"
