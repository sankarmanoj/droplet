
from socket import *
import time
import sys
import timeit
from threading import Thread
from time import sleep
rport = 25555
sport=25556
my_ip = ""
count = 0
uri = sys.argv[-1]
if "sha1_hash" in uri:
    hash = uri.partition("=")[-1]
else:
    hash = "**HASH**"
print "Searching for file with hash :" + hash
def config():
    try:
        file = open("C:/droplet/dpl/networks.txt  ", "r+")
    except:
        file = open("C:/droplet/dpl/networks.txt", "w+")
    networks = []
    data = "adf"
    while data != "":
        data = file.readline()
        data = data.strip(" \n")
        networks.append(data)
    print networks
    return networks[:-1]

running = True
def find(networks):
    for netip in networks:
        netbytes = netip.split(".")
        netbytes[-1] = 0
        receiver = socket(AF_INET, SOCK_DGRAM)
        tosend = str(netbytes[0]) + "." + str(netbytes[1]) + "." + str(netbytes[2]) + "."
        for i in xrange(1, 255):
            receiver.sendto("alive", (tosend + str(i), rport))
    print "Exit Find"
    running = False


def meet(drop_uri,send_hash):
    finder = socket(AF_INET, SOCK_DGRAM)
    finder.bind(('', sport))
    start = time.time()
    dat = ""
    global running
    avail_ip=[]
    print "Loop started"
    while (time.time() - start) < 10 and running:
        try:
            finder.settimeout(10)
            data, addr = finder.recvfrom(1024)
            print data,
            print addr
        except:
            pass
        if "available" in data:
            recv_hash = data.split(":")[1]
            if recv_hash == send_hash:
                print "Hash Available"
                avail_ip.append(addr[0])

        if addr:
            if data == "alive":
                finder.sendto(drop_uri,addr)
    print "Exit meet"
    return avail_ip
    finder.close()
	
def download(ips,theHash):
	s = socket()
	s.connect((ips[0],12345))
	print s.recv(1023)
	s.send(theHash)
	fil = s.recv(1000)
	file_path = s.recv(1000)
	file_name = s.recv(1000)
	path = file_path+"/"+"droplet_"+file_name
	print path
	f=open(path,'wb+')
	data =""
	size = 0
	done = 0 
	file_size = int(fil)
	print file_size
	print "file size is ",file_size
	while size<file_size:
		data  =s.recv(file_size/3)
		size += len(data)
		done =  size*100/(file_size)
		f.write(data)
	print "Done Writing"
	f.close()

networks = config()

i = Thread(target = find, args= (networks,))
i.start()
ips= meet(uri,hash)
download(ips,hash)
sleep(3)