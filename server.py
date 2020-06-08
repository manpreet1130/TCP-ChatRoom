import socket
import threading
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(5)

HEADERSIZE = 10

clients = []
usernames = []

def broadcast(message):
	if len(clients) == 0:
		return
	for client in clients:
		client.send(message)


def handle(client):
	while True:
		message = client.recv(1024).decode('utf-8')
		if message[HEADERSIZE:] == "exit":
			index = clients.index(client)
			username = usernames[index]
			broadcast("{} has left the chat!".format(username))
			clients.remove(client)
			usernames.remove(username)
			client.close()
			break
		broadcast(message)


def run():
	while True:
		conn, addr = server.accept()
		print("Connection established {} | {}".format(addr[0], addr[1]))
		conn.send("USER")
		username = conn.recv(1024).decode('utf-8')
		clients.append(conn)
		usernames.append(username)
		broadcast("{} has joined the chat!".format(username))
	
		thread = threading.Thread(target = handle, args = (conn,))
		thread.start()

if __name__ == "__main__":
	run()
