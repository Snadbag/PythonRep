from netmiko import ConnectHandler

IP = "158.193.152.166" # CISCO Router
USER = "admin"
PASS = "Admin123"

router_config = {
	"device_type": "cisco_ios",
	"host": IP,
	"username": USER,
	"password": PASS,
	"port": 22
}

router = ConnectHandler(**router_config)

#output = router.send_command("sh ip int brief")

conf_set = [
	"int loopback20",
	"ip add 193.168.58.32 255.255.255.255",
	"no sh"
]

output = router.send_config_set(conf_set)
print(output)