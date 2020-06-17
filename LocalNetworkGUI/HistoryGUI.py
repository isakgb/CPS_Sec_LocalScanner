## 2. window

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.history import HistoryArchive
from util.macvendor import MacVendorsApi
from datetime import datetime

class HistoryGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        ##list setting
        self.historyList = QListWidget(self)
        self.historyList.setGeometry(QRect(20, 20, 761, 380))
        self.historyList.setAutoFillBackground(True)
        self.historyList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.historyList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.historyList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.historyList.setAutoScrollMargin(14)
        self.historyList.setEditTriggers(QAbstractItemView.CurrentChanged)
        self.historyList.setObjectName("historyList")
        self.historyList.setStyleSheet("border-color: gray;")


        # load trusted names
        trusted_names = {}
        with open("trusted", 'r') as f:
            for line in f.readlines():
                if "=" in line:
                    mac, name = line.split("=")
                    trusted_names[mac] = name.strip()


        # load the history
        num_scans, host_list = HistoryArchive.get_instance().get_processed_data()
        macvendors = MacVendorsApi.get_instance()
        i=0
        for host_mac, host_data in host_list.items():
            text_lines = []
            vendor = macvendors.get_vendor(host_mac)
            name = trusted_names.get(host_mac, None)
            text_lines.append("{} ({})".format(host_mac, vendor))
            text_lines.append("    Last seen: " + datetime.fromtimestamp(int(host_data["last_seen"])).astimezone().strftime("%Y-%m-%d %I:%M %p"))
            text_lines.append("    First seen: " + datetime.fromtimestamp(int(host_data["first_seen"])).astimezone().strftime("%Y-%m-%d %I:%M %p"))
            text_lines.append("    Ports:")
            for port_data in host_data["ports"]:
                text_lines.append("        {}:".format(port_data["port_id"]))
                text_lines.append("            Last seen open: {}".format(datetime.fromtimestamp(int(port_data["last_open"])).astimezone().strftime("%Y-%m-%d %I:%M %p")))
                text_lines.append("            Port open time: {:.1f} %".format(100*  port_data["times_seen"]/host_data["times_seen"]))
            text_lines.append("")

            item = QListWidgetItem()
            item.setText("\n".join(text_lines))
            item.setBackground(QColor(245,245,245) if i % 2 == 0 else QColor(230,230,230))
            self.historyList.addItem(item)
            i+=1

        # window
        self.setWindowTitle("History")
        self.setGeometry(400, 100, 801, 420)
        self.show()



if __name__ == '__main__':
    app2 = QApplication(sys.argv)
    dialog = HistoryGUI()
    sys.exit(app2.exec_())
