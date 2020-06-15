

class NetworkInterface:
    def __init__(self):
        self.ipv4 = None
        self.subnet_mask = None
        self.name = None

    def __str__(self):
        return "[NetworkInterface {} ip={} subnet_mask={}]".format(self.name, self.ipv4, self.subnet_mask)

    def __repr__(self):
        return self.__str__()

    def get_nmap_arg(self):
        """
            Returns the nmap argment to scan this network as a string. Example output: 192.168.0.1/24
        """
        subnet_bits = 0
        for octet in self.subnet_mask.split("."):
            octet = int(octet)
            while octet > 0:
                subnet_bits += octet & 1
                octet >>= 1
        return "{}/{}".format(self.ipv4, subnet_bits)
