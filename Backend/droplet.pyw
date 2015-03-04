import subprocess
import csv

def start_pickhash():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',stdout=subprocess.PIPE,universal_newlines=True)
	num =0
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'pickhash.exe':
			num+=1
	if num ==1:
		pass
	elif num ==0:
		subprocess.Popen("start /b \"\" \"C:\\Program Files (x86)\\droplet\\pickhash.exe\"", shell=True, stdout=subprocess.PIPE)
		start_pickhash()
	else:
		for x in range(0,num-1):
			subprocess.call('taskkill /f /im pickhash.exe',shell = True,stdout=subprocess.PIPE)
		start_pickhash()
def start_sender():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',stdout=subprocess.PIPE,universal_newlines=True)
	num =0
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'sender.exe':
			num+=1
	if num ==1:
		pass
	elif num ==0:
		subprocess.Popen("start /b \"\" \"C:\\Program Files (x86)\\droplet\\sender.exe\"", shell=True, stdout=subprocess.PIPE)
		start_sender()
	else:
		for x in range(0,num-1):
			subprocess.call('taskkill /f /im sender.exe',shell = True,stdout=subprocess.PIPE)
		start_sender()

start_pickhash()
start_sender()