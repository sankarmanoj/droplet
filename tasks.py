import subprocess
import csv
def check_pick():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',stdout=subprocess.PIPE,universal_newlines=True)
	found = False
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'pickhash.exe':
			found = True
	return found
print check_pick()