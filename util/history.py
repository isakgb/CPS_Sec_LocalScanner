import json
from pathlib import Path
import datetime


class HistoryArchive:

    instance = None

    def __init__(self, history):
        self.history = history
        HistoryArchive.instance = self

    @staticmethod
    def get_instance():
        if HistoryArchive.instance is not None:
            return HistoryArchive.instance
        if Path("history.json").exists():
            history_dict = json.load(open("history.json", "r"))
            return HistoryArchive(history_dict)
        return HistoryArchive({})

    def add_scan(self, hosts):
        key = int(datetime.datetime.now().timestamp())
        print("key =", key)
        hosts_as_dict = [h.to_dict() for h in hosts]
        self.history[key] = {"type" : "scan", "hosts": hosts_as_dict}

        with open("history.json", "w") as f:
            json.dump(self.history, f)
