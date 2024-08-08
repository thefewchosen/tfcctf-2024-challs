FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    socat \
    libgmp-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install ecdsa pycryptodome

RUN useradd -m ctf
WORKDIR /home/ctf

COPY --chown=ctf:ctf server.py .

EXPOSE 1338

USER ctf

CMD socat TCP-LISTEN:1338,reuseaddr,fork EXEC:"python3 server.py"
