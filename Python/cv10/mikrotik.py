from paramiko import SSHClient, AutoAddPolicy

IP = "158.193.152.176"
USER = "admin"
PASS = "Admin123"

client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())

client.connect(hostname=IP, port=22, username=USER, password=PASS)

stdin, stdout, stderr = client.exec_command("export")
print(stdout.read().decode('utf-8'))

#for line in stdout:
	#print(line.strip("\n"))
