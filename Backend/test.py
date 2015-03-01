import subprocess
#subprocess.call("start /b \"\" \"C:\\Program Files (x86)\\droplet\\sender.exe\"",shell=False)
subprocess.Popen("start /b \"\" \"C:\\Program Files (x86)\\droplet\\sender.exe\"", creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,shell=True)