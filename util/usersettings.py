import json
from pathlib import Path

class UserSettings:

    instance = None

    def __init__(self, settings):
        print("Loading userSettings with")
        self.settings = settings
        UserSettings.instance = self
        self.interface = self.settings["interface"]

    @staticmethod
    def get_instance():
        if UserSettings.instance is not None:
            return UserSettings.instance
        if Path("usersettings.json").exists():
            macvendors_dict = json.load(open("usersettings.json", "r"))
            return UserSettings(macvendors_dict)
        return UserSettings({})

    def add_scan(self, hosts):
        pass
