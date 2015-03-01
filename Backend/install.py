import os
import shutil
import sys
import _winreg
import errno
import ctypes
import subprocess
from time import sleep

FILE_ATTRIBUTE_HIDDEN = 0x02

if sys.platform == "win32":
	path = "C:\\droplet\\" 
	system_folder = "C:\\Program Files (x86)\\droplet\\"
	config=path+"config\\"
else:
	print "Platform Not Supported"
	print "Multi-platform support will be added soon"
	print "Contact us for further information"
	sleep(10)
	sys.exit(0)
try:
	os.makedirs(path)
except OSError as e:
	print type(e.errno)
	if e.errno==5 or e.errno==13:
		print "Installation Failed 1"
		print "Please run as an ADMINISTRATOR"
		sleep(10)
		sys.exit(0)
		pass
try:
	os.makedirs(config)#By this point you are already admin but just to be safe... and lazy.
except OSError as e:
	if e.errno ==5 or e.errno==13:
		print "Installation Failed 2"
		print "Please run as an ADMINISTRATOR"
		sleep(10)
		sys.exit(0)
		pass
	else:
		print "Error. "
		print "Please contact an administrator and say ERROR NUMBER 3 and error "+str(e.errno)+". It is very important to correct this error now and in further releases"
		sleep(1)
ret = ctypes.windll.kernel32.SetFileAttributesW(ur"C:\\droplet\\config",FILE_ATTRIBUTE_HIDDEN)
if ret ==0:
	raise ctypes.WinError()
if not os.path.isdir(system_folder):
	try:
		os.makedirs(system_folder)
	except OSError as e:
		if e.errno == 5 or e.errno==13:
			print "Installation Failed 3"
			print "Please run as an ADMINISTRATOR"
			pass
		else:
			print "Error. Installation Failed"
			print "Please contact an administrator and say ERROR NUMBER 4 and error "+str(e.errno)+". It is very important to correct this error now and in further releases"
		print "Cleaning up..."
		shutil.rmtree(path)
		print "Done."
		sleep(10)
		sys.exit(0)
files=[ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f))]
for f in files:
	if f != "networks":
		try:
			shutil.copy(f,system_folder)
		except IOError as e:
			if e.errno==13 or e.errno==5:
				print "Installation Failed 4"
				print "Please run as an ADMINSTRATOR"
			else:
				print "Error. Installation Failed"
				print "Please contact an administrator and say ERROR NUMBER 5 and error "+str(e.errno)+". It is very important to correct this error now and in further releases"
			print "Cleaning up..."
			shutil.rmtree(path)
			print "Done."
			sleep(10)
			sys.exit(0)
			
shutil.copy("networks",config)
#shutil.copy("upload.py",system_folder)
#shutil.copy("hola.py",system_folder)
#shutil.copy("run.exe",system_folder)

_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, 'drop\\shell\\open\\command')
_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,'drop\\DefaultIcon')
rkey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,r'drop',0,_winreg.KEY_WRITE)
_winreg.SetValue(rkey,r"shell\open\command",_winreg.REG_SZ,'"'+system_folder+'run.exe" "%1"')
_winreg.SetValue(rkey,"",_winreg.REG_SZ,"URL:drop Protocol")
_winreg.SetValueEx(rkey,"URL Protocol",0,_winreg.REG_SZ,"")
stkey= _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",0,_winreg.KEY_ALL_ACCESS)
_winreg.SetValueEx(stkey,"Droplet_sender",0,_winreg.REG_SZ,'"'+system_folder+'sender.exe"')
_winreg.SetValueEx(stkey,"Droplet_hashing",0,_winreg.REG_SZ,'"'+system_folder+'hashing.exe"')

#os.system("bckghashing.vbs")###subprocess is better
#os.system("bckgsender.vbs")###subprocess is better

###REmove and run
os.system("start /b \"\" \"C:\\Program Files (x86)\\droplet\\pickhash.exe\"")
os.system("start /b \"\" \"C:\\Program Files (x86)\\droplet\\sender.exe\"")
shutil.copy("exp.bat",os.environ['appdata']+r"\Microsoft\Windows\Start Menu\Programs\Startup")
print "Installation Success"
print "Start downloading files from the website! Please remember to allow firewall access to the programs when they run for the first time"
sleep(10)