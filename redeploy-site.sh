#!/bin/bash

tmux kill-server

cd pe-portfolio-site
git fetch && git reset origin/main --hard

source env/bin/activate
pip install -r requirements.txt

tmux new-session -d -s portfolio 'flask run --host=0.0.0.0 --port=80'
