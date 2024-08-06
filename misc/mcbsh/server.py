import subprocess
import os
import uuid

def menu():
    print("[+] Hello h4ck3r!")
    print()
    print()
    print("[ANNOUNCEMENT] THIS SERVICE IS UNDER INVESTIGATION")
    print("[ANNOUNCEMENT] BY THE FBI AND THE NSA! ANY COMMAND")
    print("[ANNOUNCEMENT] YOU ENTER WILL BE LOGGED AND USED ")
    print("[ANNOUNCEMENT] AGAINST YOU IN THE COURT OF LAW!")
    print()
    print()
    print("[133333333337] It's your friend [REDACTED]. I ")
    print("[133333333337] managed to fly under their radar")
    print("[133333333337] and get you this backdoor shell")
    print("[133333333337] on theserver, but you have to get")
    print("[133333333337] creative.")
    print()
    print()

def prompt():
    return input("root@????????$ ")

def sanitize(command):
    whitelist = ['#', '$', "'", "(", ")", "0", "1", "<", "\\"]

    for c in command:
        if c not in whitelist:
            return False
    return True

def tmp_file():
    return os.path.join('/tmp', str(uuid.uuid4()))

def main():
    menu()
    while True:
        
        inp = prompt()
        if not sanitize(inp):
            print("[ERROR] Malicious input detected!")
            print("[!!!!!] THIS WILL BE REPORTED")
            exit()
        
        aux = tmp_file()
        with open(aux, 'w') as f:
            f.write(inp)
            f.close()
        
        cmd = f"cat {aux} | bash"

        output, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        print(output.decode())


if __name__ == '__main__':
    main()
