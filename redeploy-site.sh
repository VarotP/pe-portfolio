#!/usr/bin/bash

tmux kill-session -t flask-app 2>/dev/null
tmux new-session -d -s flask-app

tmux send-keys -t flask-app "cd pe-portfolio" C-m
tmux send-keys -t flask-app "git fetch && git reset --hard origin/main" C-m
tmux send-keys -t flask-app "source python3-virtualenv/bin/activate" C-m
tmux send-keys -t flask-app "pip install -r requirements.txt" C-m
tmux send-keys -t flask-app "flask run --host=0.0.0.0" C-m

echo "Deployment complete"
