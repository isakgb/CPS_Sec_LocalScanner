import json
from pathlib import Path
from network.host import Host

class Whitelist:

    instance = None
    filename = "whitelist.json"

    def __init__(self, cache):
        print("Loading whitelist with", cache)
        self.cache = cache
        self.whitelist = self.cache["whitelist"]
        self.semiwhitelist = self.cache["semiwhitelist"]
        self.blacklist = self.cache["blacklist"]
        Whitelist.instance = self

    @staticmethod
    def get_instance():
        if Whitelist.instance is not None:
            return Whitelist.instance
        if Path(Whitelist.filename).exists():
            d = json.load(open(Whitelist.filename, "r"))
            return Whitelist(d)
        return Whitelist({"whitelist":[], "semiwhitelist" : {}, "blacklist" : []})

    def save(self):
        with open(Whitelist.filename, "w") as f:
            json.dump(self.cache, f)

    def add_semiwhitelisted(self, host: Host):
        self.semiwhitelist[host.mac_address] = [x.port_id for x in host.ports]
        self.save()

    def remove_semiwhitelisted(self, mac):
        if mac in self.semiwhitelist:
            del self.semiwhitelist[mac]
            self.save()


