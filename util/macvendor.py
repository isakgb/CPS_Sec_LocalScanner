import json
from pathlib import Path
import requests
from time import sleep

class MacVendorsApi:

    instance = None

    def __init__(self, cache):
        self.cache = cache
        MacVendorsApi.instance = self

    @staticmethod
    def get_instance():
        if MacVendorsApi.instance is not None:
            return MacVendorsApi.instance
        if Path("macvendors.json").exists():
            macvendors_dict = json.load(open("macvendors.json", "r"))
            return MacVendorsApi(macvendors_dict)
        return MacVendorsApi({})

    def get_vendor(self, mac_address):
        if mac_address is None:
            return None
        if mac_address in self.cache:
            return self.cache[mac_address]
        sleep(0.5) # Prevent getting rate limited
        res = requests.get("https://api.macvendors.com/{}".format(mac_address))
        if (res.status_code < 300 and res.status_code >= 200):
            vendor = res.text
            self.cache[mac_address] = vendor
            with open("macvendors.json", "w") as f:
                json.dump(self.cache, f)
            return vendor
        else:
            print("Failed to get from macvendors api, status code", res.status_code, res.text)

