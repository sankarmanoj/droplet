from socket import *
from threading import Thread
from time import sleep,time
s= socket()
port = 12345

def download(ips,theHash):
	s.connect((ips[0],port))
	print s.recv(1023)
	s.send(theHash)
	fil = s.recv(1000)
	file_path = s.recv(1000)
	file_name = s.recv(1000)
	path = file_path+"/"+"droplet_"+file_name
	print path
	f=open(path,'ab+')
	data =""
	size = 0
	done = 0 
	file_size = int(fil)
	print file_size
	print "file size is ",file_size
	while done <100:
		start  = time()
		data  =s.recv(file_size/3)
		size += len(data)
		done =  size*100/(file_size)
		start = time()
		f.write(data)
	print "Done Writing"
	f.close()
ips = ['192.168.0.3']
download(ips,'24be595dea1df611285e8f2c15f44b19cc4faa9d')