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
        self.nmap_installed = None
        #raise TypeError("Cannot create NetworkScanner. Use NetworkScanner.create()")

    def scan_network(self, network_interface: NetworkInterface, port_scan=False) -> List[Host]:
        nmap_args = ["nmap"]
        if not port_scan:
            nmap_args.append("-sn")
        nmap_args.append(network_interface.get_nmap_arg())
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

    def scan_network_callback(self, network_interface: NetworkInterface, callback, port_scan=False):
        """
        Starts an asynchronous (non-blocking) network scan on the given network interface. When the scan is complete
        the callback will be called with the list of hosts as the argument. Port scanning can be enabled by setting
        port_scan to True.

        :param network_interface: A NetworkInterface object corresponding to the network interface you want to scan.
        :param callback: A function taking a list of Host objects as an argument that will be called when the scan
        is completed.
        :param port_scan: Whether or not to port scan each host. Defaults to False.
        """
        def scan_network_with_callback():
            scan_result = self.scan_network(network_interface, port_scan=port_scan)
            callback(scan_result)

        threading.Thread(target=scan_network_with_callback).start()


    @staticmethod
    def create():
        """
        Creates and returns a NetworkScanner instance. If this a Unix-like system, returns an instance of NetworkScannerUnixLike,
        and if this is a Windows system, returns an instance of NetworkScannerWindows.

        :return: An instance of NetworkScanner for this operating system
        """
        # Figure out if this is a unix-like or windows system, and return the appropriate scanner instance

        return NetworkScanner()
        try:
            run(["ifconfig", "--version"], stdout=PIPE)
            print("OS is Unix-like")
            return NetworkScannerUnixlike()
        except FileNotFoundError as e:
            pass

        try:
            run(["ipconfig", "--version"], stdout=PIPE)
            print("OS is Windows")
            return NetworkScannerWindows()
        except FileNotFoundError:
            print("Found neither ipconfig nor ifconfig")

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
        d = run("ifconfig --version", stdout=PIPE)
        print("return code", d.returncode)
        print(d.stdout.decode())
    except FileNotFoundError as e:
        print("Failed to find nmap. Is it installed? ({})".format(e.strerror))