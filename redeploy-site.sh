#!/bin/bash

# Change directory to your project folder
cd ./portfolio-site

# Fetch latest changes from GitHub main branch and reset local repository
git fetch && git reset origin/main --hard

python -m venv python3-virtualenv
source python3-virtualenv/bin/activate

pip install -r requirements.txt

systemctl restart myportfolio
