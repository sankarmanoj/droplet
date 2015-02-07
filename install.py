import os
import shutil
import sys
import _winreg
from time import sleep
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
	path = "/droplet/"
elif _platform == "darwin":
	path = "/droplet/"
elif _platform == "win32":
	path = "C:\\droplet\\" 
	system_folder = "C:\\Program Files (x86)\\droplet\\"
try:
	os.makedirs(path)
except:
	pass
try:
	os.makedirs(path+"dpl/")
except:
	pass	
if not os.path.isdir(system_folder):
	try:
		os.makedirs(system_folder)
	except:
		print "Installation Failed"
		print "Please run as an administrator"
		sleep(10)
		sys.exit(0)
#shutil.copy("download.py",system_folder)
#shutil.copy("upload.py",system_folder)
#shutil.copy("hola.py",system_folder)
#shutil.copy("run.exe",system_folder)
_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT, 'drop\\shell\\open\\command')
_winreg.CreateKey(_winreg.HKEY_CLASSES_ROOT,'drop\\DefaultIcon')
rkey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,r'drop',0,_winreg.KEY_WRITE)
_winreg.SetValue(rkey,r"shell\open\command",_winreg.REG_SZ,'"'+system_folder+'run.exe" "%1"')
_winreg.SetValue(rkey,"",_winreg.REG_SZ,"URL:drop Protocol")
_winreg.SetValueEx(rkey,"URL Protocol",0,_winreg.REG_SZ,"")