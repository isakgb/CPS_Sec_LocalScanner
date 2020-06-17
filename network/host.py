from typing import List
from util.macvendor import MacVendorsApi

class Host:
    def __init__(self):
        self.ports: List[Port] = []
        self.mac_address = None
        self.ip_address = None

    def get_GUI_name(self):
        return "IP: {}, MAC: {} ({})".format(self.ip_address, self.mac_address, MacVendorsApi.get_instance().get_vendor(self.mac_address))

    def to_dict(self):
        ports = [{"port_id": x.port_id, "service": x.service, "protocol": x.protocol} for x in self.ports]
        return {"ports": ports, "mac_address" : self.mac_address, "ip_address": self.ip_address}

    @staticmethod
    def from_dict(d):
        host = Host()
        host.mac_address = d["mac_address"]
        host.ip_address = d["ip_address"]
        host.ports = [Port(p["port_id"], p["service"], p["protocol"]) for p in d["ports"]]
        return host


class Port:
    def __init__(self, port_id, service, protocol):
        self.port_id = port_id
        self.service = service
        self.protocol = protocol


    def __repr__(self):
        return "[Port {}/{} {}]".format(self.port_id, self.protocol, self.service)

    def __str__(self):
        return self.__repr__()