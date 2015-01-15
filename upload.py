from socket import *
import os
from threading import Thread
from time import sleep
s= socket()
port = 12345
def update_hashes():
	file = open('C:/droplet/dpl/hashes.txt','r')
	hashes = file.read().splitlines()[1:]
	hashes= [hash.split('~') for hash in hashes]
	file.close()
	return hashes


sent= 0

def send(c,data,size):
	global sent
	
	sent += c.send(data)
	print (sent*100)/size
def handler(c):
	
	c.send("accepted")
	hashes = update_hashes()
	print "Waiting for hash"
	h= c.recv(1024)
	print h
	for hash in hashes:
		if hash[0] == h:
			path = hash[1]
			size = os.path.getsize(path)
			c.send(str(size))
			name = os.path.split(path)
			print name
			f = open(path,'rb')
			c.send(name[0])
			sleep(0.1)
			c.send(name[1])
			sleep(0.1)
			while True: 
				
				sleep(0.1)
				data = f.read()
				if not data:
					break
				Thread(target=send(c,data,size)).start()
			print "Broke"
			c.close()
			f.close()
			sleep(1)
			break
	

		
 
def uploader():
	hostname = gethostname()
	ip =  gethostbyname(hostname)
	s.bind((ip,12345))
	s.listen(5)
	while True:
		c,addr= s.accept()
		handler(c)
		print "Done handling"
		
uploader()
