#!/bin/bash

# Kill all existing tmux sessions
tmux kill-session -t flask-server 2>/dev/null

# Change directory to your project folder
cd ./portfolio-site
# pwd
# Fetch latest changes from GitHub main branch and reset local repository
git fetch && git reset origin/main --hard

python -m venv python3-virtualenv

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s flask-server \; \
    send-keys "export FLASK_ENV=development" C-m \; \
    send-keys "flask run --host=0.0.0.0" C-m
