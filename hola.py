from socket import *
from time import sleep

rport = 25555
sport = 25556
def add_ip(ip, ips):
    if (ip not in ips):
        with open("ip.txt", "a") as myfile:
            myfile.write(ip + "\n")
        return True
    else:
        return False
def update_hashes():
    try:
        hfile = open("C:/droplet/dpl/hashes.txt","r+")
    except:
        hfile = open("C:/droplet/dpl/hashes.txt","w+")
    hashes = hfile.read().splitlines()
    hfile.close()
    hashes = [new.partition("~")[0] for new in hashes]
    return hashes

try:
    nfile = open("C:/droplet/dpl/networks.txt","r+")
except:
    nfile = open("C:/droplet/dpl/networks.txt","w+")
a = socket(AF_INET, SOCK_DGRAM)
a.bind(('', rport))
data = ""
ips = nfile.read().splitlines()
nfile.close()

while data != "q":
    data, addr = a.recvfrom(1024)
    if "drop" in data and "sha1_hash" in data:
        hash = data.partition("=")[-1]
        print "Received hash request for ", hash
        hashes = update_hashes()		
        if hash in hashes:
            print "File available"
            a.sendto("available:"+hash,(addr[0],sport))
        else:
            print "File not available"
    if (data == "alive"):
        print "Got Alive"
        a.sendto("alive", (addr[0], sport))
        add_ip(addr[0],ips)

a.close()



