import _winreg
import ctypes
import errno
import os
import shutil
import sys
import time


###Unneeded imports to facilitate py2exe
import cPickle
import collections
import csv
import hashlib
import socket
import subprocess
import threading
###


FILE_ATTRIBUTE_HIDDEN = 0x02

if sys.platform == "win32":
	path = "C:\\droplet\\" 
	system_folder = "C:\\Program Files (x86)\\droplet\\"
	config=path+"config\\"
else:
	print "Platform Not Supported"
	print "Multi-platform support will be added soon"
	print "Contact us for further information"
	time.sleep(10)
	sys.exit(0)
	
try:
	os.makedirs(system_folder)
except OSError as e:
	if e.errno == 5 or e.errno==13:
		print "Installation Failed 1"
		print "Please run as an ADMINISTRATOR"
		time.sleep(10)
		sys.exit(0)
	elif e.errno==17:
		try:
			print "You have droplet previously installed. Clearing up in 5 seconds"
			os.startfile(os.path.join(os.getcwd(),"killall.exe"))
			print "All ready. Installing now..."
			time.sleep(5)
			shutil.rmtree(system_folder)
			os.makedirs(system_folder)
		except OSError as newe:
			if newe.errno == 5 or newe.errno==13:
				print "Installation Failed 1"
				print "Please run as an ADMINISTRATOR"
				time.sleep(10)
				sys.exit(0)
			print "Error. Installation Failed 1"
			print "RE-RUN THE INSTALLER. If error persists please contact an administrator and say ERROR NUMBER 1 and error "+str(newe.errno)+". It is very important to correct this error now and in further releases"
			time.sleep(10)
			sys.exit(0)
	else:
		print "Error. Installation Failed 1"
		print "RE-RUN THE INSTALLER. If error persists please contact an administrator and say ERROR NUMBER 2 and error "+str(e.errno)+". It is very important to correct this error now and in further releases"
		time.sleep(10)
		sys.exit(0)
flag=1	
try:
	os.makedirs(path)
except OSError as e:
	if e.errno==5 or e.errno==13:
		print "Installation Failed 2"
		print "Please run as an ADMINISTRATOR"
	elif e.errno==17:
		flag=0
	else:
		print "Error. Installation Failed 2"
		print "RE-RUN THE INSTALLER. If error persists please contact an administrator and say ERROR NUMBER 3 and error "+str(e.errno)+". It is very important to correct this error now and in further releases"
	if flag==1:
		print "Cleaning up..."
		try:
			shutil.rmtree(system_folder)
			print "Done. State : 1RESET"
		except:
			print "Problem during clean-up 1. Run as an ADMINISTRATOR. If problem persists contact us."
		time.sleep(10)
		sys.exit(0)
		
try:
	os.makedirs(config)#By this point you are already admin but just to be safe... and lazy.
except OSError as e:
	flag2=1
	if e.errno ==5 or e.errno==13:
		print "Installation Failed 3"
		print "Please run as an ADMINISTRATOR"
	elif e.errno==17:
		try:
			shutil.rmtree(config)
			os.makedirs(config)
			flag2=0
		except OSError as newe:
			print "Error. Installation Failed 3"
			print "RE-RUN THE INSTALLER. If error persists please contact an administrator and say ERROR NUMBER 4 and error "+str(newe.errno)+". It is very important to correct this error now and in further releases"
	else:
		print "Error. Installation Failed 3"
		print "RE-RUN THE INSTALLER. If error persists please contact an administrator and say ERROR NUMBER 5 and error "+str(e.errno)+". It is very important to correct this error now and in further releases"
	if flag2==1:
		print "Cleaning up..."
		try:
			shutil.rmtree(system_folder)
			if flag==1:
				shutil.rmtree(path)
				print "Done. State : 2RESET"
			print "3RESET"
		except:
			print "Problem during clean-up 2. Run as an ADMINISTRATOR. If problem persists contact us."
		time.sleep(10)
		sys.exit(0)

ret = ctypes.windll.kernel32.SetFileAttributesW(ur"C:\\droplet\\config",FILE_ATTRIBUTE_HIDDEN)
if ret ==0:
	raise ctypes.WinError() #And then what?

files=[ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f))]
for f in files:
	if f != "networks":
		try:
			shutil.copy(f,system_folder)
		except IOError as e:
			if e.errno==13 or e.errno==5:
				print "Installation Failed 4"
				print "Please run as an ADMINISTRATOR"
			else:
				print "Error. Installation Failed 4"
				print "RE-RUN THE INSTALLER. If error persists please contact an administrator and say ERROR NUMBER 6 and error "+str(e.errno)+" with file "+e.filename+" . It is very important to correct this error now and in further releases"
				print "Cleaning up..."
			try:
				shutil.rmtree(system_folder)
				if flag==1:
					shutil.rmtree(path)
					print "Done. State : 4RESET"
				print "5RESET"
			except:
				print "Problem during clean-up 3. Run as an ADMINISTRATOR. If problem persists contact us."
			time.sleep(10)
			sys.exit(0)
			
shutil.copy("networks",config)

_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, 'drop\\shell\\open\\command')
_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,'drop\\DefaultIcon')
rkey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,r'drop',0,_winreg.KEY_WRITE)
_winreg.SetValue(rkey,r"shell\open\command",_winreg.REG_SZ,'"'+system_folder+'run.exe" "%1"')
_winreg.SetValue(rkey,"",_winreg.REG_SZ,"URL:drop Protocol")
_winreg.SetValueEx(rkey,"URL Protocol",0,_winreg.REG_SZ,"")

shutil.copy("droplet.exe",os.environ['appdata']+r"\Microsoft\Windows\Start Menu\Programs\Startup")
os.startfile(system_folder+"droplet.exe")

print "\n\nInstallation Success!!"
print "Start downloading files from the website! Please remember to allow firewall access to the programs when they run for the first time"
time.sleep(10)