from socket import *
def version_control():
	v = socket()
	v.bind(("",12346))
	v.listen(5)
	while True:
		c,addr= v.accept()
		h=c.recv(1024);
		if h=="Send version now":
			c.send(current_version);
		else:
			c.send("Error");