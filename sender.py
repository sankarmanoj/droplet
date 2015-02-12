from socket import *
from time import sleep
import os
import sys
from threading import Thread
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
s= socket()
port = 12345
send_size = 500
def add_ip(ip, ips):
    if (ip not in ips):
        with open(ip_path, "a") as myfile:
            myfile.write(ip + "\n")
        return True
    else:
        return False
def uhashes():
    try:
        hfile = open(hash_path,"r+")
    except:
        hfile = open(hash_path,"w+")
    hashes = hfile.read().splitlines()
    hfile.close()
    hashes = [new.partition("~")[0] for new in hashes]
    return hashes
def UDP_Listener():
	try:
		nfile = open(network_path,"r+")
	except:
		nfile = open(network_path,"w+")
	a = socket(AF_INET, SOCK_DGRAM)
	a.bind(('', rport))
	data = ""
	ips = nfile.read().splitlines()
	nfile.close()

	while True:
		data, addr = a.recvfrom(1024)
		if "drop" in data and "sha1_hash" in data:
			hash = data.partition("=")[-1]
			print "Received hash request for ", hash
			hashes = uhashes()		
			if hash in hashes:
				print "File available"
				a.sendto("available:"+hash,(addr[0],sport))
			else:
				print "File not available"
		if (data == "alive"):
			print "Got Alive"
			a.sendto("alive", (addr[0], sport))
			add_ip(addr[0],ips)
def update_hashes():
	file = open(hash_path,'r')
	hashes = file.read().splitlines()[1:]
	hashes= [hash.split('~') for hash in hashes]
	file.close()
	print hashes
	return hashes
def send_text(input):
		input_text = str(input)
		send_text = input_text + "-"*(send_size-len(input_text))
		return send_text
def handler(c):
	sent = 0
	path = ""
	available = False
	while True:
		command = c.recv(send_size).strip('-')
		if(command ==""):
			break
		print command
		if (command == "info"):
			hashes = update_hashes()	
			h = c.recv(send_size).strip('-')
			for hash in hashes:
				if hash[0] == h:
					path = hash[1]
					available = True
					size = str(os.path.getsize(path))
					size_send = size + "-"*(send_size-len(size))
					c.send(size_send)
					print size
					name = os.path.split(path)[-1]
					print path
					name_send = name + "-"*(send_size-len(name))
					c.send(name_send)
			
			if not available:
				c.send("0")
				sleep(0.1)
				c.send("0")
		if(command=="quit"):
			c.close()
			break 
		if(command =="init_download"):
			print "got init download"
			seekTo =0 
			seekRecv = False
			sizeRecv = False
			if(path ==""):
				c.send(send_text('file_not_init'))
			else:
				c.send(send_text('ready'))
				FiletoSend = open(path,'rb')
				got = c.recv(send_size).strip('-')
				print "got = ",got
				if(got=="seek"):
					seekTo = int(c.recv(send_size).strip('-'))
				got = c.recv(send_size).strip('-')
				print "got = ",got
				if(got=="size"):
					readSize = int(c.recv(send_size).strip('-'))
				print 'willsend'
				c.send(send_text('willsend'))
				print "seek = ",seekTo,"  size= ",readSize
				FiletoSend.seek(seekTo)
				toSend = FiletoSend.read(readSize)
				print len(toSend)
				print c.sendall(toSend)
def uploader():
	hostname = gethostname()
	ip =  gethostbyname(hostname)
	s.bind((ip,12345))
	s.listen(5)
	while True:
		c,addr= s.accept()
		handler(c)
		print "Done handling"
Thread(target = UDP_Listener).start()
uploader()



