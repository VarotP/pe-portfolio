#!/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1
git fetch && git reset --hard origin/main
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl restart myportfolio

echo "Deployment complete"
