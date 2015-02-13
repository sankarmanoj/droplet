import os
import shutil
import sys
import _winreg
from os import listdir,getcwd
from os.path import isfile, join
from time import sleep
from sys import platform as _platform
import ctypes
FILE_ATTRIBUTE_HIDDEN = 0x02

if _platform == "win32":
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
except:
	pass
try:
	os.makedirs(config)
except:
	pass	
ret = ctypes.windll.kernel32.SetFileAttributesW(ur"C:\\droplet\\config",FILE_ATTRIBUTE_HIDDEN)
if ret ==0:
	raise ctypes.WinError()
if not os.path.isdir(system_folder):
	try:
		os.makedirs(system_folder)
	except:
		print "Installation Failed"
		print "Please run as an administrator"
		sleep(10)
		sys.exit(0)
files=[ f for f in listdir(getcwd()) if isfile(join(getcwd(),f))]
for f in files:
	if f != "networks":
		shutil.copy(f,system_folder)
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
