from subprocess import run, PIPE
from network.networkinterface import NetworkInterface
from typing import List
import threading
from network.host import Host, Port
import psutil
from util.usersettings import UserSettings
import socket


class NetworkScanner():

    def __init__(self):
        pass

    def scan_network(self, network_interface: NetworkInterface, port_scan=False) -> List[Host]:
        nmap_args = ["nmap", "-T5"]
        if not port_scan:
            nmap_args.append("-sn")
        nmap_args.append(network_interface.get_nmap_arg())
        print("Starting scan \"{}\"".format(" ".join(nmap_args)))
        nmap_result = run(nmap_args, stdout=PIPE)

        next_host = None

        hosts = []

        for line in nmap_result.stdout.decode().split("\n"):
            if len(line) == 0:
                continue
            if "Nmap scan report" in line:
                ip = line.split()[-1]
                if next_host is not None:
                    hosts.append(next_host)
                next_host = Host()
                next_host.ip_address = ip
            elif "/tcp" in line or "/udp" in line:
                port, state, service = line.split()
                if state == "open":
                    port_num, protocol = port.split("/")
                    next_host.ports.append(Port(port_num, service, protocol))
            elif "MAC Address" in line:
                mac = line.split()[2]
                next_host.mac_address = mac

        hosts.append(next_host)

        return hosts

    def scan_network_callback(self, callback, network_interface: NetworkInterface = None, port_scan=False):
        """
        Starts an asynchronous (non-blocking) network scan on the given network interface. When the scan is complete
        the callback will be called with the list of hosts as the argument. Port scanning can be enabled by setting
        port_scan to True.

        :param network_interface: A NetworkInterface object corresponding to the network interface you want to scan. Default:
        network interface given by get_network_interface()
        :param callback: A function taking a list of Host objects as an argument that will be called when the scan
        is completed.
        :param port_scan: Whether or not to port scan each host. Defaults to False.
        """
        if network_interface is None:
            network_interface = self.get_network_interface()

        def scan_network_with_callback():
            scan_result = self.scan_network(network_interface, port_scan=port_scan)
            callback(scan_result)

        threading.Thread(target=scan_network_with_callback).start()


    def get_network_interface(self) -> NetworkInterface:
        """
        Gets the active local interface with name specified form usersettings.json

        :return: NetworkInterface objects
        """
        interfaces = psutil.net_if_addrs()
        chosen_interface = UserSettings.get_instance().interface
        ipv4_interface = next((x for x in interfaces[chosen_interface] if x.family == socket.AF_INET))
        nif = NetworkInterface()
        nif.name = UserSettings.get_instance().interface
        nif.ipv4 = ipv4_interface.address
        nif.subnet_mask = ipv4_interface.netmask
        return nif


def check_nmap_installed():
    try:
        d = run("nmap --version", stdout=PIPE)
        print("return code", d.returncode)
        print(d.stdout.decode())
    except FileNotFoundError as e:
        print("Failed to find nmap. Is it installed? ({})".format(e.strerror))
