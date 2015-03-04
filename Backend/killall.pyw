import subprocess
import csv

def killall():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',stdout=subprocess.PIPE,universal_newlines=True)
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'pickhash.exe':
			subprocess.call('taskkill /f /im pickhash.exe',shell = True,stdout=subprocess.PIPE)
		elif p['Image Name'] == 'sender.exe':
			subprocess.call('taskkill /f /im sender.exe',shell = True,stdout=subprocess.PIPE)
killall()