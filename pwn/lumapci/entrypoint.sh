#/bin/bash

/qemu/bin/qemu-system-x86_64 \
	-m 256M \
	-kernel /bzImage \
	-initrd /initramfs.cpio.gz \
	-display none \
	-append "console=ttyS0" \
	-serial stdio  \
	-device lumapci \
	-monitor none,server,nowait,nodelay,reconnect=-1 \
	-no-reboot
