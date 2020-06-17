import json
from pathlib import Path

class UserSettings:

    instance = None
    filename = "usersettings.json"

    def __init__(self, settings):
        self.settings = settings
        UserSettings.instance = self
        self.interface = self.settings["interface"]
        self.mon_disabled_interface = self.settings["mon_disabled_interface"]
        self.mon_enabled_interface = self.settings["mon_enabled_interface"]
        self.ap_mac_address = self.settings["ap_mac_address"]
        if not Path(UserSettings.filename).exists():
            with open(UserSettings.filename, "w") as f:
                print(UserSettings.filename, "not found. It has been created with default values. Please change them")
                json.dump(self.settings, f, indent=2)

    @staticmethod
    def get_instance():
        if UserSettings.instance is not None:
            return UserSettings.instance
        if Path("usersettings.json").exists():
            d = json.load(open("usersettings.json", "r"))
            return UserSettings(d)
        return UserSettings({"interface": "<enter network interface to scan>",
                             "mon_disabled_interface": "<enter network interface to use for monitor mode e.g. wlan0>",
                             "mon_enabled_interface": "<enter network interface name for monitoring when its enabled e.g wlan0mon>",
                             "ap_mac_address": "<enter mac address of access point for deauth attack. find with iwconfig>"})
