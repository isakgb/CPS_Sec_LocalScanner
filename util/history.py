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

    def get_processed_data(self):
        data = {}

        num_scans = 0

        for timestamp, obj in self.history.items():
            timestamp = int(timestamp)
            if obj["type"] != "scan":
                continue
            num_scans += 1
            hosts = obj["hosts"]
            for host in hosts:
                host_data = data.get(host["mac_address"], {"last_seen": timestamp, "first_seen": timestamp, "trusted_since": None, "ports":[],  "times_seen":0})
                host_data["times_seen"] += 1
                host_data["last_seen"] = max(int(host_data["last_seen"]), timestamp)
                host_data["first_seen"] = min(int(host_data["first_seen"]), timestamp)
                for port in host["ports"]:
                    id = port["port_id"]
                    ports_data = host_data["ports"]
                    port_data = next((p for p in ports_data if p["port_id"] == id), None)
                    if port_data == None:
                        port_data = {"port_id": id, "last_open": timestamp, "times_seen": 0}
                        ports_data.append(port_data)
                    port_data["times_seen"] += 1
                    port_data["last_open"] = max(int(port_data["last_open"]), timestamp)
                data[host["mac_address"]] = host_data
        return num_scans, data




