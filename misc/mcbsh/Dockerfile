FROM ubuntu:22.04

# Install the necessary packages
RUN apt update && apt install -y socat python3

# Create a user
RUN useradd ctf

# Switch to the user
USER ctf

WORKDIR /home/ctf

# Copy the challenge files

COPY server.py .
COPY flag.txt .

# Expose the port

EXPOSE 1337

# Run the server
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 server.py",pty,stderr

# Build the image
# docker build -t mcbsh .

# Run the container
# docker run -d -p 1337:1337 mcbsh