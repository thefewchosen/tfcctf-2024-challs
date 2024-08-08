from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256, Public_key, Private_key
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes,bytes_to_long

FLAG = b'TFCCTF{y0u_end3D_Th3_c0rruption}'

G = generator_256
order = G.order()
rand = random.randint(1,order-1)
pubkey = Public_key(G, rand*G)
privkey = Private_key(pubkey, rand)



messages = [
    "Initiate phase two, we've secured new access points.",
    "Encryption keys updated. Proceed with the new protocol.",
    "Ensure all communications are routed through the secure channel.",
    "Begin the new vote manipulation sequence at dawn.",
    "The second wave of votes is in. Validate and proceed.",
    "Our agents are in place. Execute the next steps discreetly.",
    "Double-check all encrypted transmissions for vulnerabilities.",
    "We've detected interference. Activate the countermeasures.",
    "Final preparations complete. Awaiting your signal.",
    "The rigging algorithm is updated. Deploy immediately."
]


a = 733113379677
b = 657
m = 2 ** 150
state = random.randint(0,2**150-1)
def patched_random():
    global a,state,b,m
    state = (a * state + b) % m


def the_random():
    patched_random()
    global state
    nonce = ((random.getrandbits(106) & (random.getrandbits(106) ^ random.getrandbits(106)) | random.getrandbits(106)) << 150) | state
    #print(nonce,nonce>>11)
    return nonce, state >> 110

def sign_message(message):
    hsh = hashlib.sha256(message.encode()).digest()
    nonce, leak = the_random()
    #print(nonce.bit_length())
    sig = privkey.sign(bytes_to_long(hsh), nonce)
    return {"hash": bytes_to_long(hsh), "r": hex(sig.r), "s": hex(sig.s), "leak": leak}

max_used = 50
used = 0
print('What do you want to do?')
print('1. Listen in on conversation')
print('2. Submit the info you found')
print('3. Get pubkey')
while True:
    data = input()

    if data == '1':
        if used > max_used:
            print('Why do you need to sign more than 50 times?')
            exit()

        message = messages[random.randint(0,len(messages)-1)]
        print(sign_message(message))
        used+=1

    if data == '2':
        key = int(input('Key? '))

        if key == rand:
            print('At last, they are gone, as payment you receive the flag.')
            print(FLAG)
        exit()

    if data == '3':

        print('Too easy if i just give it to you right? Try and solve this, i need P.x and Q.x')

        # Sage just refused to work in docker, so ill give you the values 
        # from sage.all import GF,EllipticCurve,randrange

        # curve secp256r1
        # p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        # a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
        # b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        # F = GF(p)
        # E = EllipticCurve(F, [a, b])
        # G = E((0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5))
        
        # # random numbers, dont give to remote
        # k1 = 75380278515850780003422743857805513644121843952557579815527313277653333116728
        # k2 = 44951229054644063143553819213636174740174542207343728047061846610226274787858
        # P = k1 * G
        # Q = k2 * G
        # print(P,Q)
        # for i in range(2):
        #     a,b = random
        #     out.append([a,b,a * P + b * Q])

        # out = [[96782493581107017213287940431906781117775401216029818502421722067004869671128, 18538871412723353247501824844190723767417562653982776603661341114579966744605, (36566315207713245091176405415710241138207929913023468223244125431056706761511 : 10976749572513729423697994197166601856770738841401887139027157647878298794556 : 1)], [90010878197235881814460760613107101266952873141567869967076779247935202848887, 95977587327198575377209621701343555951978156791715802180542478952260780398694, (42891521857367877217539705137361753088078433669344096955944120767916016902990 : 24699094435692184568058588241787734516749698041094295443543822154915466799108 : 1)]]

        received = input().split(' ')

        # dont give to remote
        px_good, qx_good = 925622415864520877674801785058948523363582457913737697143172270385292253499, 10653238890983401517678086577588980515868586289190149296648223248933435682661
        px, qx = int(received[0]), int(received[1])
        
        if px_good == px and qx_good == qx:
            print(f'Public key: {int(pubkey.point.x())} {int(pubkey.point.y())}')

        else:
            print('Wrong ma friend')
            exit()