import sys
from LocalNetworkGUI.Home_IoT_Security import MyApp, QApplication
from util.macvendor import MacVendorsApi


def nmap_result_callback(hosts):
    print("scan finished")
    for host in hosts:
        vendor = MacVendorsApi.get_instance().get_vendor(host.mac_address)
        print("Found host", host.ip_address, "with MAC address", host.mac_address, vendor)
        print("  ports: ")
        for port in host.ports:
            print("    ", port.port_id, port.protocol, port.service)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())