import socket
import json
from enum import IntEnum

SERVER = "127.0.0.1"
PORT = 8080
MLEN = 1000
QUEUE_LENGTH = 10

class Operacia(IntEnum):
	LOGIN = 1
	EXIT = 2
	USERS = 3
	MSG = 4

class Message:
	def __init__(self, paOd, paKomu, paOperacia, paText):
		self.od = paOd
		self.komu = paKomu
		self.operacia = paOperacia
		self.text = paText

	def to_bytes(self):
		json_str = json.dumps(self.__dict__)
		return json_str.encode

	@staticmethod
	def json_decoder(paObj):
		return Message(paObj['od'], paObj['komu'], paObj['operacia'], paObj['text'])

def napoveda():
	print("NAPOVEDA:")
	print("\t\q ukonci program")
	print("\t\l vypise pouzivatelov")
	print("\t\h help")
	print("\tSpravu posielajte v tvare: prijemca:sprava")

print("CHAT CLIENT")
od = input("Zadaj meno: ")
napoveda()

sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))

msg = Message(od, "Server", Operacia.LOGIN.value, None)
sock.send(msg.to_bytes())

while True:
	text = input("Zadajte spravu alebo \ pre specialnu operaciu:")
	if text[0] == '\\':
		if text[1] == 'h':
			napoveda()
			continue
		elif text[1] == 'q':
			break
		elif text[1] == 'l':
			msg = Message(od, "Server", Operacia.USERS.value, None)
			sock.send(msg.to_bytes())
			server_msg = sock.recv(1000)
			msg = json.loads(server_msg.decode(), object_hooks = Message.json_decoder)
			print("Zoznam použivatelov: {}".format(msg.text))
			continue
	msg_array = text.split(":")
	msg = Message(od, msg_array[0], Operacia.MSG.value, msg_array[1])
	sock.send(msg.to_bytes())

msg = Message(od, "Server", Operacia.EXIT.value, None)
sock.send(msg.to_bytes())

sock.close()