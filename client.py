import socket
import threading
import sys

connection = socket.socket()
host = socket.gethostname()
port = 9999

connection.connect((host, port))

HEADERSIZE = 10
online = True
username = raw_input("USERNAME (upto {} digits) : ".format(HEADERSIZE))

def receive():
	while online:
		try:
			message = connection.recv(1024).decode('utf-8')
			if message == "USER":
				connection.send(username)
			else:
				print(message)
		
		except:
			print("An error occured!")
			connection.close()

def write():
	global online
	while True:
		mess = raw_input()
		message = "{:>{}}".format(username + "> ", HEADERSIZE) + mess
		connection.send(message)
		if mess == "exit":
			online = False
			connection.close()
			sys.exit()

	
if __name__ == "__main__":
	write_thread = threading.Thread(target = write)
	receive_thread = threading.Thread(target = receive)	

	receive_thread.start()
	write_thread.start()

