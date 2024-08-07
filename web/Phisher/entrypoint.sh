#!/bin/bash

service nginx start

# Start the web app
cd /app/dashboard && python3 ./main.py &

# Start the mail app
cd /app/mail && python3 ./main.py
