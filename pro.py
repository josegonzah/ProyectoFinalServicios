import os 
from sys import argv, exit

if len(argv) != 2:
    print("you are idiot")
    exit(1)

ip = str(argv[1])
c1 =  'python3 store.py "' + ip + '" & python3 bank.py "' + ip + '" & python3 bank_udp.py "' + ip + '"'
os.system(c1)