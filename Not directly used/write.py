from threading import Thread
from time import sleep
file = open("a.txt","w+")
def write(pos):

	file.seek(pos)
	sleep(1)
	file.write("Hello")
i = Thread(target = write(0))
u = Thread(target = write(10))
i.start()
u.start()