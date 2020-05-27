from subprocess import run, PIPE
from network.networkinterface import NetworkInterface
from typing import List


class NetworkScanner():

    def __init__(self):
        self.nmap_installed = None
        raise TypeError("Cannot create NetworkScanner. Use NetworkScanner.create()")

    @staticmethod
    def create():
        """
        Creates and returns a NetworkScanner instance. If this a Unix-like system, returns an instance of NetworkScannerUnixLike,
        and if this is a Windows system, returns an instance of NetworkScannerWindows.

        :return: An instance of NetworkScanner for this operating system
        """
        # Figure out if this is a unix-like or windows system, and return the appropriate scanner instance
        try:
            run("ifconfig --version", stdout=PIPE)
            print("OS is Unix-like")
            return NetworkScannerUnixlike()
        except FileNotFoundError:
            pass

        try:
            run("ipconfig --version", stdout=PIPE)
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


def check_nmap_installed():
    try:
        d = run("ifconfig --version", stdout=PIPE)
        print("return code", d.returncode)
        print(d.stdout.decode())
    except FileNotFoundError as e:
        print("Failed to find nmap. Is it installed? ({})".format(e.strerror))


scanner = NetworkScanner.create()
s = scanner.get_network_interfaces()

print(s[0].get_nmap_arg())