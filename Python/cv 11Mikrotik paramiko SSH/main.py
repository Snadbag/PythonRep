from flask import Flask, Response, jsonify, request
from paramiko import SSHClient, AutoAddPolicy
import json
import requests
from requests.auth import HTTPBasicAuth

IP = "158.193.152.176"
USER = "admin"
PASS = "Admin123"

HOST = "0.0.0.0"
PORT = "8080"

app = Flask(__name__)

client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect(hostname=IP, port=22, username=USER, password=PASS)

stdin, stdout, stderr = client.exec_command("export")
print(stdout.read().decode('utf-8'))

#for line in stdout:
	#print(line.strip("\n"))

@app.route('/')
def index():
	stdin, stdout, stderr = client.exec_command("export")
	
	temp = "<h1>Mikrotik " + IP + " exports</h1>"
	for line in stdout:
		temp += "<span>" + line + "</span><br>"

	temp += "<h1>IP Addresses</h1>"
	temp += show_addresses()

	print(show_addresses())
	return temp

def show_addresses():
	response = requests.get('http://158.193.152.176/rest/ip/address', auth=HTTPBasicAuth(USER, PASS), verify=False)

	addr_list = ""
	for add in response.json():
		addr_list += f"{add['address']} (int: {add['actual-interface']}, network: {add['network']})<br>"

	return addr_list

# main
if __name__ == "__main__":
	app.run(HOST, PORT)