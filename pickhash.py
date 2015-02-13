import cPickle as pickle
from os import listdir
from os.path import isfile,join,getmtime
import hashlib,time
from time import sleep
from sys import platform as _platform
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
def get_files():
	files=[pathfordroplet+f for f in listdir(pathfordroplet) if isfile(join(pathfordroplet,f))]
	return files
def sha1_hash(file):
	BLOCKSIZE = 65536
	print "Hashing ",file
	hasher = hashlib.sha1()
	try:
		with open(file, 'rb') as afile:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
		a=hasher.hexdigest()
		return a
	except:
		return 1
	
def full_hash():
	files = get_files()
	hashes=[]
	for f in files:
		hashes.append([sha1_hash(f),f])	
	write_hashes(hashes)
	return hashes
def write_hashes(hashes):
	pickle.dump(hashes,open(hash_path,"wb+"))
def read_hashes():
	try:
		hashes = pickle.load(open(hash_path,"rb+"))
		return hashes
	except:
		return full_hash()
def check_update():
	files = get_files()
	hashed_files = []
	hash =[]
	hashes = read_hashes()
	for h in hashes:
		hashed_files.append(h[-1])
		hash.append(h[0])
	changed = False
	for f in files:
		if f not in hashed_files:
			
			changed = True
			new_hash = sha1_hash(f)
			if new_hash ==1 :
				break
			if new_hash in hash:
				hashes[hash.index(new_hash)][1]=f
			else:
				hashes.append([new_hash,f])
			break
	for h in hashed_files:
		if h not in files:
			hashes.pop(hashed_files.index(h))
			changed = True
	if (changed):
		
		write_hashes(hashes)

while True:
	check_update()
	sleep(0.01)

	
