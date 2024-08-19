FROM ubuntu:24.04 as qemu_builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y build-essential git
RUN apt install -y python3 python3-venv ninja-build pkgconf libglib2.0-dev

WORKDIR /build
RUN git clone --depth=1 --branch=v9.0.2 https://github.com/qemu/qemu.git qemu
WORKDIR /build/qemu


COPY ./qemu/0001-Challenge-commit.patch .
RUN git apply 0001-Challenge-commit.patch 

RUN ./configure --without-default-features --prefix=/custom_qemu --target-list=x86_64-softmmu
RUN make -j16 install

# =====================================================
FROM ubuntu:24.04 as linux_builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y build-essential libncurses-dev bison flex libssl-dev libelf-dev git bc

WORKDIR /build
RUN git clone --depth=1 --branch=v6.10 https://github.com/torvalds/linux.git linux
WORKDIR /build/linux 

# Dirty me daddy
RUN echo " " >> README

RUN make defconfig
RUN make -j16 bzImage

RUN cp arch/x86/boot/bzImage /build/bzImage

# ======================================================
FROM alpine:latest as userspace

RUN apk add base64 vim

COPY ./userspace/init /init

# ======================================================
FROM ubuntu:24.04 as userspace_builder

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y cpio gzip

WORKDIR /build/rootfs

COPY --from=userspace / .

RUN find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz

# ======================================================
FROM ubuntu:24.04

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

COPY --from=linux_builder /build/bzImage /
COPY --from=qemu_builder /custom_qemu /qemu
COPY --from=userspace_builder /build/initramfs.cpio.gz /

RUN /usr/sbin/useradd --no-create-home -u 6969 ctf

RUN apt update -y 
RUN apt upgrade -y
RUN apt install -y libglib2.0-dev socat

COPY ./flag.txt /flag.txt

WORKDIR /home/ctf

RUN chown -R root:root /home/ctf
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

USER ctf
EXPOSE 1337
ENTRYPOINT ["/tini", "--"]
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/home/ctf/entrypoint.sh",pty,setsid,setpgid,stderr,ctty
