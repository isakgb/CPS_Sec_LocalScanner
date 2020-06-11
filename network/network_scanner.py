from subprocess import run, PIPE
from network.networkinterface import NetworkInterface
from typing import List
import threading
from network.host import Host, Port

class NetworkScanner():

    def __init__(self):
        self.nmap_installed = None
        raise TypeError("Cannot create NetworkScanner. Use NetworkScanner.create()")

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

    def get_network_interfaces(self) -> List[NetworkInterface]:
        """
        Gets a list of active local network interfaces

        :return: List of NetworkInterface objects
        """
        raise NotImplementedError()


class NetworkScannerWindows(NetworkScanner):

    def __init__(self):
        pass

    def get_network_interfaces(self):

        def get_nonempty_lines(ipconfig_output):
            for output_line in ipconfig_output.split("\r\n"):
                if len(output_line) > 0 and output_line != "Windows IP Configuration":
                    yield output_line

        ipconfig_result = run("ipconfig", stdout=PIPE).stdout.decode()

        next_nif = None
        nifs = []

        for line in get_nonempty_lines(ipconfig_result):
            if line[:3] != "   ":
                if next_nif is not None:
                    nifs.append(next_nif)
                next_nif = NetworkInterface()
                next_nif.name = line
            else:
                if "Media disconnected" in line:
                    next_nif.disconnected = True
                elif "IPv4 Address" in line:
                    next_nif.ipv4 = line.split(" : ")[1]
                elif "Subnet Mask" in line:
                    next_nif.subnet_mask = line.split(" : ")[1]
                elif "Default Gateway" in line:
                    next_nif.default_gateway = line.split(" : ")[1]

        nifs = [nif for nif in nifs if not nif.disconnected]

        return nifs


class NetworkScannerUnixlike(NetworkScanner):
    def __init__(self):
        pass

    def get_network_interfaces(self):
        # TODO: Implement this feature on non-Windows systems

        ipconfig_result = run("ifconfig", stdout=PIPE).stdout.decode()

        # Split each interface

        nifs = []

        for line in ipconfig_result.split("\n"):
            print(line.encode())


def check_nmap_installed():
    try:
        d = run("ifconfig --version", stdout=PIPE)
        print("return code", d.returncode)
        print(d.stdout.decode())
    except FileNotFoundError as e:
        print("Failed to find nmap. Is it installed? ({})".format(e.strerror))