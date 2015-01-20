from os import listdir
from os.path import isfile,join,getmtime
import hashlib,time
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
	hash_path = "/droplet/dpl/hashes"
	pathfordroplet = "/droplet/"
elif _platform == "darwin":
	hash_path = "/droplet/dpl/hashes"
	pathfordroplet = "/droplet/"
elif _platform == "win32":
	pathfordroplet = "C:/droplet/"
	hash_path = "C:/droplet/dpl/hashes.txt"
def rehash():
	files=[ f for f in listdir(pathfordroplet[:-1]) if isfile(join(pathfordroplet[:-1],f))]
	files=[ pathfordroplet + f for f in files]

	if files:
		print "Rehashing"
		#hashing
		for file in files:
			a= sha1_hash(file)
			with open(hash_path,"a+") as writehash:
				writehash.write("\n"+a +"~"+file)
		print "Done Rehashing"
	else:
		print "Aww, We can't find your droplet. Download files using the droplet website "
		quit()

def sha1_hash(file):
	BLOCKSIZE = 65536
	print file
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
		read_name =	open(hash_path,"r+")
	except:
		return False
	names= read_name.read().splitlines()
	names = [name.split("~")[1] for name in names if "~" in name]
	files=[ f for f in listdir(pathfordroplet) if isfile(join(pathfordroplet,f))]
	files=[ pathfordroplet + f for f in files]
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
			del_line_file(hash_path,hash)
			with open(hash_path,"a+") as writehash:
				writehash.write(hash+"~"+file+"\n")
			print "ends"
		else:
			print "filedel"
			for x in abcd:
				try:
					names.remove(x)
				except:
					pass
			f = open(hash_path,"r")
			lines= f.read().splitlines()
			f.close()
			
			f = open(hash_path,"w")
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
		hfile=open(hash_path,"r+")
	except:
		hfile=open(hash_path,"w+")
	lines =  hfile.read().splitlines()
	hfile.close()
	if lines:
		file_change(pathfordroplet)
	else:
		rehash()
	time.sleep(0.001)