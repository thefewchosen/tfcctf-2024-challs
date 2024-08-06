FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    socat \
    libstdc++6 \
    libgcc-s1 \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/ctf

COPY virtual /home/ctf/virtual
COPY flag.txt /home/ctf/flag.txt
COPY game.txt /home/ctf/game.txt

RUN chmod +x /home/ctf/virtual

WORKDIR /home/ctf

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:/home/ctf/virtual
