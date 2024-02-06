from threading import Thread
import socket
import json as json
from enum import IntEnum

SERVER = "0.0.0.0"
PORT = 8080
MLEN = 1000
QUEUE_LENGTH = 10

class Operacia(IntEnum):
	LOGIN = 1
	EXIT = 2
	USERS = 3

class Message:
	def __init__(self, paOd, paKomu, paOperacia, paText):
		self.od = paOd
		self.komu = paKomu
		self.operacia = paOperacia
		self.text = paText

	@staticmethod
	def json_decoder(paObj):
		return Message(paObj['od'], paObj['komu'], paObj['operacia'], paObj['text'])

def HandleClient(clientSocket, clientAddress, users):
	while(True):
		json = clientSocket.recv(MLEN)
		jsonString = json.decode()
		message = json.loads(jsonString, ojbect_hook = Message.json_decoder)

		if message.operacia == Operacia.LOGIN:
			users.append(message.od)
			print("Prihlasil sa {} z IP {}:{}".format(message.od, clientAddress[0], clientAddress[1]))
			continue

		elif message.operacia == Operacia.EXIT:
			users.remove(message.od)
			print("Odhlasil sa {} z IP {}:{}".format(message.od, clientAddress[0], clientAddress[1]))
			return

		elif message.operacia == Operacia.USERS:
			response = Message("SERVER", message.od, Operacia.USERS.value, users)
			jsonString = json.dumps(response.__dict__)
			clientSocket.send(jsonString.encode())
			continue

		elif message.operacia == Operacia.MSG:
			print("Správa od {} komu {} text:".format(message.od, message.komu, message.text))

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((SERVER, PORT))
	sock.listen(QUEUE_LENGTH)

	users = list()
	
	print("SERVER UP!")

	while True:
		(clientSocket, clientAddress) = sock.accept()
		thread = Thread(target = HandleClient, args = (clientSocket, clientAddress, users))
		thread.start()