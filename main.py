from network.network_scanner import NetworkScanner
from util.macvendor import MacVendorsApi


def nmap_result_callback(hosts):
    print("scan finished")
    for host in hosts:
        vendor = MacVendorsApi.get_instance().get_vendor(host.mac_address)
        print("Found host", host.ip_address, "with MAC address", host.mac_address, vendor)
        print("  ports: ")
        for port in host.ports:
            print("    ", port.port_id, port.protocol, port.service)


scanner = NetworkScanner.create()

nif = scanner.get_network_interface()

print("Found network interface:", nif)


scanner.scan_network_callback(nif, nmap_result_callback, port_scan=True)
print("Network scan started asynchronously")
print(nif.get_nmap_arg())
