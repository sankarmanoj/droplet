import subprocess
import csv
def check_sender():
	p_tasklist = subprocess.Popen('tasklist.exe /fo csv',universal_newlines=True)
	num =0
	print "hello"
	print p_tasklist.communicate()
	for p in csv.DictReader(p_tasklist.stdout):
		if p['Image Name'] == 'sender.exe':
			num+=1
		if num ==1:
			print "only 1"
			return True
		elif num ==0:
			print "not open"
			return False
		else:
			print "killing"
			subprocess.call('taskkill /f /im sender.exe',shell = True)
			return False
check_sender()