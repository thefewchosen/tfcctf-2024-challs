# Solution

This is a side-channel attack. The program sleeps 3 seconds after every correct character. First we need to find the correct length - the output will change when a long enough argument is passed. Then bruteforce the characters one by one