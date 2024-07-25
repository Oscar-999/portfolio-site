#!/bin/bash

# Change directory to your project folder
cd ./portfolio-site

# Fetch latest changes from GitHub main branch and reset local repository
git fetch && git reset origin/main --hard

# Spin down existing containers to avoid out-of-memory issues
docker compose -f docker-compose.prod.yml down

# Rebuild and start the containers in detached mode
docker compose -f docker-compose.prod.yml up -d --build
