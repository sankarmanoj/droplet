from socket import *
from time import sleep,time
import os
import sys
from threading import Thread
from sys import platform as _platform
import cPickle as pickle
import subprocess
import csv

Release_Version = "1"


if _platform == "win32":
	pathfordroplet = "C:/droplet/"
	system_folder = "C:\\Program Files (x86)\\droplet\\"
	hash_path =  "C:\\droplet\\config\\hashes"
	network_path = "C:\\droplet\\config\\networks"
else:
		print "Platform Not Supported"
		print "Multi-platform support will be added soon"
		print "Contact us for further information"
		sleep(10)
		sys.exit(0)
rport = 25555
sport = 25556
s = socket()
port = 12345
send_size = 500
start=time()

def check_pick():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',stdout=subprocess.PIPE,universal_newlines=True)
	num =0
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'pickhash.exe':
			num+=1
	if num ==1:
		return True
	elif num ==0:
		return False
	else:
		subprocess.call('taskkill /f /im pickhash.exe',shell = True)
		return False
def pickhashchecker(now=0):
		if (now==1 or (now==0 and time()-start>3600)):
			if not check_pick():
				try:
					os.system("start /b \"\" \"C:\\Program Files (x86)\\droplet\\pickhash.exe\"")
					start=time()
					return True
				except:
					return False
			else:
				return True	
def uhashes():
	hashes = pickle.load(open(hash_path,"rb+"))
	hash = [h[0] for h in hashes]
	return hash
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
		if "vrequest" in data:
			if pickhashchecker(1):
				a.sendto(Release_Version,addr)
			else:
				a.sendto("-1",addr)
		if "drop" in data and "sha1_hash" in data:
			hash = data.partition("?")[0].partition("=")[-1]
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
			
def update_hashes():
	try:
		hashes = pickle.load(open(hash_path,"rb+"))
		return hashes
	except:
		pass
def send_text(input):
		input_text = str(input)
		send_text = input_text + "-"*(send_size-len(input_text))
		return send_text
def handler(c):
	sent = 0
	path = ""
	command = "input"
	available = False
	while command != "":
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
	s.bind(("",12345))
	s.listen(5)
	while True:
		c,addr= s.accept()
		Thread(target=handler(c)).start()
		print "Done handling"
Thread(target = UDP_Listener).start()
uploader()



