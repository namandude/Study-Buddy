#!/bin/bash
# Install ffmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# Start Flask
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=$PORT
