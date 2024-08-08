with open("flag.txt", "r") as f:
    d = f.read()
    # make into hex
    d = d.encode("utf-8").hex()
    # add c after every character
    d = "c".join(d)
    print(d)