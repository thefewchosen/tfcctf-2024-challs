#!/bin/bash

# Generate 16 random characters
random_chars=$(openssl rand -base64 24 | tr -dc 'a-zA-Z0-9')

# Create the entry
entry="1 admin $random_chars admin@mcsky.ro 69420"

# Write the entry to db.txt
echo "$entry" > /home/ctf/db.txt
echo "2 bob siminaaremere bob@mcsky.ro 20" >> /home/ctf/db.txt