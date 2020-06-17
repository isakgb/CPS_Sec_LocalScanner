import json
from pathlib import Path

class UserSettings:

    instance = None

    def __init__(self, settings):
        self.settings = settings
        UserSettings.instance = self
        self.interface = self.settings["interface"]

    @staticmethod
    def get_instance():
        if UserSettings.instance is not None:
            return UserSettings.instance
        if Path("usersettings.json").exists():
            d = json.load(open("usersettings.json", "r"))
            return UserSettings(d)
        return UserSettings({})

    def add_scan(self, hosts):
        pass
