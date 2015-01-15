from os import listdir
from os.path import isfile,join,getmtime
import hashlib,time

def rehash():
	pathfordroplet = "C:/droplet"
	files=[ f for f in listdir(pathfordroplet) if isfile(join(pathfordroplet,f))]
	files=[ "C:/droplet/" + f for f in files]

	if files:
		print "Rehashing"
		#hashing
		for file in files:
			a= sha1_hash(file)
			with open("C:\droplet\dpl\hashes.txt","a+") as writehash:
				writehash.write("\n"+a +"~"+file)
		print "Done Rehashing"
	else:
		print "Aww, We can't find your droplet. Download files using the droplet website -\n\t\t\t xxx.xxx.xxx.xxx"
		quit()

def sha1_hash(file):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(file, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	a=hasher.hexdigest()
	return a
	
def file_change(pathfordroplet):
	try:
		read_name =	open("C:\droplet\dpl\hashes.txt","r+")
	except:
		return False
	names= read_name.read().splitlines()
	names = [name.split("~")[1] for name in names if "~" in name]
	files=[ f for f in listdir(pathfordroplet) if isfile(join(pathfordroplet,f))]
	files=[ "C:/droplet/" + f for f in files]
	if set(names)==set(files):
		return False
	else:
		abcd=set(files)
		for x in names:
			try:
				files.remove(x)
			except:
				pass
		if files:
			print "filemod"
			file = files[0]
			hash = sha1_hash(file)
			del_line_file("C:\droplet\dpl\hashes.txt",hash)
			with open("C:\droplet\dpl\hashes.txt","a+") as writehash:
				writehash.write(hash+"~"+file+"\n")
			print "ends"
		else:
			print "filedel"
			for x in abcd:
				try:
					names.remove(x)
				except:
					pass
			f = open("C:\droplet\dpl\hashes.txt","r")
			lines= f.read().splitlines()
			f.close()
			
			f = open("C:\droplet\dpl\hashes.txt","w")
			for line in lines:
				if line=="":
					f.write("\n")
				elif line.split("~")[1]!=names[0]:
					f.write(line)
			f.close()
			print "ends"
					
def del_line_file(file,hashtoDel):
	f = open(file,"r")
	lines = f.readlines()
	f.close()
	f = open(file,"w")
	for line in lines:
		if line.split("~")[0]!=hashtoDel:
			f.write(line)
while True:
	
	try:
		hfile=open("C:\droplet\dpl\hashes.txt","r+")
	except:
		hfile=open("C:\droplet\dpl\hashes.txt","w+")
	lines =  hfile.read().splitlines()
	hfile.close()
	if lines:
		file_change("C:/droplet")
	else:
		rehash()
	time.sleep(0.001)