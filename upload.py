from socket import *
import os
from threading import Thread
from time import sleep
import sys
s= socket()
port = 12345
send_size = 500
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
	hash_path = "/droplet/dpl/hashes"
elif _platform == "darwin":
	hash_path = "/droplet/dpl/hashes"
elif _platform == "win32":
	hash_path = "C:/droplet/dpl/hashes.txt"
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
#	hostname = gethostname()
#	ip =  gethostbyname(hostname)		### I had Vmnet8 enabled and its ip was stored. Problem.
	ip = "10.3.1.175"
	s.bind((ip,12345))
	s.listen(5)
	while True:
		c,addr= s.accept()
		print "Someone has connected"
		handler(c)				#c is the client who has connected.
		print "Done handling"
		
uploader()
#python C:\Code\droplet\out.py drop:sha1_hash=d91d0805a09886d8840d2052a86a01c1fac907ef