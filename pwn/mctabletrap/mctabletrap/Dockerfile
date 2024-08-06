FROM ubuntu:22.04

RUN apt update
RUN apt install -y socat netcat net-tools gdb

RUN useradd ctf 

WORKDIR /home/ctf
COPY ./chall /home/ctf/
COPY ./create_db.sh /home/ctf/
COPY ./flag.txt /home/ctf/

RUN chown -R ctf:ctf /home/ctf
RUN chmod +x /home/ctf/chall
RUN chmod +x /home/ctf/create_db.sh

EXPOSE 1337

USER ctf

RUN /home/ctf/create_db.sh
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:./chall,stderr

# sudo docker compose up --build