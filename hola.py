from socket import *
from time import sleep
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    hash_path = "/droplet/dpl/hashes"
    network_path = "/droplet/dpl/networks"
    pathfordroplet = "/droplet/"
elif _platform == "darwin":
    hash_path = "/droplet/dpl/hashes"
    network_path = "/droplet/dpl/networks"
    pathfordroplet = "/droplet/"
elif _platform == "win32":
    pathfordroplet = "C:/droplet/"
    hash_path = "C:/droplet/dpl/hashes.txt"
    network_path ="C:/droplet/dpl/networks.txt"
    ip_path = "C:/droplet/dpl/ip.txt"
rport = 25555
sport = 25556
def add_ip(ip, ips):
    if (ip not in ips):
        with open(ip_path, "a") as myfile:
            myfile.write(ip + "\n")
        return True
    else:
        return False
def update_hashes():
    try:
        hfile = open(hash_path,"r+")
    except:
        hfile = open(hash_path,"w+")
    hashes = hfile.read().splitlines()
    hfile.close()
    hashes = [new.partition("~")[0] for new in hashes]
    return hashes

try:
    nfile = open(network_path,"r+")
except:
    nfile = open(network_path,"w+")
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



