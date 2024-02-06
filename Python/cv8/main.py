from scapy.all import *
import struct

def mac_to_bytes(mac):
	mac_hex = mac.replace(":", "")
	return bytes.fromhex(mac_hex)

def set_bit(input, por_bit):
	return input | 1 << por_bit - 1

class Eth_hdr():
	def __init__(self, src_mac):
		self.dst_mac = "10:00:0C:CC:CC:CC"
		self.src_mac = src_mac
		self.length = 0
		self.payload = None

	def add_payload(self, payload):
		self.payload = payload
	
	def to_bytes(self):
		payload_bytes = self.payload.to_bytes()
		self.length = len(payload_bytes)
		return mac_to_bytes(self.dst_mac) + mac_to_bytes(self.src_mac) + struct.pack("!H", self.length) + payload_bytes
	
class Llc_hdr():
	def __init__(self):
		self.dsap = 0xaa
		self.ssap = 0xaa
		self.ctrl = 0x03
		self.oui = "00:00:0C"
		self.pid = 0x2000
		self.payload = None

	def add_payload(self, payload):
		self.payload = payload

	def to_bytes(self):
		return struct.pack("!3B", self.dsap, self.ssap, self.ctrl) + mac_to_bytes(self.oui) + struct.pack("!H", self.pid) + self.payload.to_bytes()

class CDP_hdr():
	def __init__(self):
		self.version = 1
		self.ttl = 180
		self.checksum = 0xabb7
		self.payload = list()

	def add_payload(self, payload):
		self.payload.append(payload)

	def to_bytes(self):
		payload_bytes = bytes()

		for tlv in self.payload:
			payload_bytes += tlv.to_bytes()

		return struct.pack("!2BH", self.version, self.ttl, self.checksum) + payload_bytes

class TLV():
	def __init__(self, type):
		self.type = type
		self.length = 4

	def to_bytes(self):
		return struct.pack("!HH", self.type, self.length)

class TLV_device_id(TLV):
	def __init__(self, hostname):
		TLV.__init__(self, 0x0001)
		hostname_bytes = hostname.encode()
		self.length += len(hostname_bytes)
		self.hostname_bytes = hostname_bytes
	
	def to_bytes(self):
		return TLV.to_bytes(self) + self.hostname_bytes

class TLV_port_id(TLV_device_id):
	def __init__(self, hostname):
		super().__init__(hostname)
		self.type = 0x0003

class TLV_software(TLV_device_id):
	def __init__(self, version):
		super().__init__(version)
		self.type = 0x0005

class TLV_capabilities(TLV):
	def __init__(self, router = False, switch = False, host = True):
		TLV.__init__(self, 0x0004)
		self.length += 4
		self.capabilities = 0

		if router:
			self.capabilities = set_bit(self.capabilities, 1)
		if switch:
			self.capabilities = set_bit(self.capabilities, 4)
		if host:
			self.capabilities = set_bit(self.capabilities, 5)
	
	def to_bytes(self):
		return TLV.to_bytes(self) + struct.pack("!I", self.capabilities)

IFACES.show()
iface = IFACES.dev_from_index(10)
sock = conf.L2socket(iface)

eth_hdr = Eth_hdr("11:22:33:44:55:66")
llc_hdr = Llc_hdr()
cdp_hdr = CDP_hdr()

tlv_device_id = TLV_device_id("davidkou")
cdp_hdr.add_payload(tlv_device_id)
tlv_port_id = TLV_port_id("wifi")
cdp_hdr.add_payload(tlv_port_id)
tlv_cap = TLV_capabilities(switch = True)
cdp_hdr.add_payload(tlv_cap)
tlv_software = TLV_software("Win11")
cdp_hdr.add_payload(tlv_software)

llc_hdr.add_payload(cdp_hdr)
eth_hdr.add_payload(llc_hdr)

sock.send(eth_hdr.to_bytes())