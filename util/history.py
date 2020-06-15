import json
from pathlib import Path

class HistoryArchive:

    instance = None

    def __init__(self, history):
        print("Loading historyarchive with")
        self.history = history
        HistoryArchive.instance = self

    @staticmethod
    def get_instance():
        if HistoryArchive.instance is not None:
            return HistoryArchive.instance
        if Path("history.json").exists():
            macvendors_dict = json.load(open("history.json", "r"))
            return HistoryArchive(macvendors_dict)
        return HistoryArchive({})

    def add_scan(self, hosts):
        pass
