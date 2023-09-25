#!/bin/bash

# Update the package list
sudo apt-get update

# Install system dependencies
sudo apt-get install -y python3-pyaudio libespeak1 mplayer

# Install Python dependencies
pip3 install -r requirements.txt
