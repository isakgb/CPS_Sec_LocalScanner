## 1. window

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from network.network_scanner import NetworkScanner
from network.deauth import DeauthHandler
from util.history import HistoryArchive
from util.whitelist import Whitelist

from LocalNetworkGUI.HistoryGUI import HistoryGUI


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.datetime = QDateTime.currentDateTime()
        self.initUI()
        self.scanner = NetworkScanner()

    def initUI(self):

        ##time status
        self.statusBar().showMessage('Updated : ' + self.datetime.toString(Qt.DefaultLocaleShortDate))

        ##list setting
        self.iotList = QListWidget(self)
        self.iotList.setGeometry(QRect(20, 80, 761, 480))
        self.iotList.setAutoFillBackground(True)
        self.iotList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.iotList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.iotList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.iotList.setAutoScrollMargin(14)
        self.iotList.setEditTriggers(QAbstractItemView.CurrentChanged)
        self.iotList.setObjectName("iotList")
        self.iotList.setStyleSheet("border-color: gray;")


        ##Scan Button
        self.scanbtn = QPushButton('Scan', self)
        self.scanbtn.setCheckable(False)
        self.scanbtn.move(20, 20)
        self.scanbtn.setIcon(QIcon('LocalNetworkGUI/scanicon.png'))
        self.scanbtn.resize(self.scanbtn.sizeHint())
        self.scanbtn.clicked.connect(self.scan_Click)
        self.scanbtn.toggle()

        ##Add Device Button
        addbtn = QPushButton('Add a device', self)
        addbtn.setCheckable(False)
        addbtn.move(115, 20)
        addbtn.setIcon(QIcon('LocalNetworkGUI/addicon.png'))
        addbtn.resize(addbtn.sizeHint())
        addbtn.clicked.connect(self.add_Click)
        addbtn.toggle()

        ##Add Semi trusted Device Button
        addbtn = QPushButton('Add a semi trusted device', self)
        addbtn.setCheckable(False)
        addbtn.move(245, 20)
        addbtn.setIcon(QIcon('LocalNetworkGUI/addicon.png'))
        addbtn.resize(addbtn.sizeHint())
        addbtn.clicked.connect(self.add_semitrusted_Click)
        addbtn.toggle()


        ##Delete Device Button
        deletebtn = QPushButton('Delete a device', self)
        deletebtn.setCheckable(False)
        deletebtn.move(436, 20)
        deletebtn.setIcon(QIcon('LocalNetworkGUI/deleteicon.png'))
        deletebtn.resize(deletebtn.sizeHint())
        deletebtn.clicked.connect(self.delete_Click)
        deletebtn.toggle()

        ##Rename Button
        renamebtn = QPushButton('Rename ', self)
        renamebtn.setCheckable(False)
        renamebtn.move(574, 20)
        renamebtn.setIcon(QIcon('LocalNetworkGUI/renameicon.png'))
        renamebtn.resize(renamebtn.sizeHint())
        renamebtn.clicked.connect(self.rename_Click)
        renamebtn.toggle()

        ##History Device Button
        historybtn = QPushButton('History', self)
        historybtn.setCheckable(False)
        historybtn.move(670, 20)
        historybtn.setIcon(QIcon('LocalNetworkGUI/historyicon.png'))
        historybtn.resize(historybtn.sizeHint())
        #historybtn.setStyleSheet('background: red;')
        historybtn.clicked.connect(self.history_Click)
        historybtn.toggle()

        ##Risk Label
        risk = QLabel(self)
        risk.resize(50, 50)
        pixmap = QPixmap("LocalNetworkGUI/riskicon.png")
        pixmap = pixmap.scaledToWidth(30)
        risk.setPixmap(QPixmap(pixmap))
        risk.move(640, 15)
        risk.hide()

        ##window
        self.setWindowTitle("Home IoT security")
        self.setWindowIcon(QIcon('LocalNetworkGUI/homeicon.png'))
        self.setGeometry(300, 200, 801, 600)
        self.show()

    ## button function

    ## add button
    def add_Click(self):
        if self.iotList.currentItem().state == 0:
            self.add_question()
        else:
            self.add_information()

    def add_question(self):
        reply = QMessageBox.question(self, 'question', 'Are you sure to add this device?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.iotList.currentItem().state = 1
            self.iotList.currentItem().setIcon(QIcon('LocalNetworkGUI/safeicon.png'))
            self.iotList.currentItem().setBackground(QColor(200, 255, 200))
            item = self.iotList.takeItem(self.iotList.currentRow())

            trust = item.text().split(' ')[3] + "\n"
            f = open('trusted', 'a')
            f.write(trust)
            f.close()

            self.iotList.addItem(item)


    def add_information(self):
        QMessageBox.information(self, 'information', 'Already Added!', QMessageBox.Ok)

    ## add semi trusted button
    def add_semitrusted_Click(self):
        if self.iotList.currentItem().state == 0:
            self.add_semitrusted_question()
        else:
            self.add_semitrusted_information()

    def add_semitrusted_question(self):
        reply = QMessageBox.question(self, 'question', 'Are you sure to add this device?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.iotList.currentItem().state = 2
            self.iotList.currentItem().setIcon(QIcon('LocalNetworkGUI/safeicon.png'))
            self.iotList.currentItem().setBackground(QColor(255, 240, 150))
            item = self.iotList.takeItem(self.iotList.currentRow())

            Whitelist.get_instance().add_semiwhitelisted(item.host)

            trust = item.text().split(' ')[3] + "\n"
            f = open('trusted', 'a')
            f.write(trust)
            f.close()

            self.iotList.addItem(item)

    def add_semitrusted_information(self):
        QMessageBox.information(self, 'information', 'Already Added!', QMessageBox.Ok)

    ## delete button
    def delete_Click(self):
        self.delete_question1()

    def delete_question1(self):
        reply = QMessageBox.question(self, 'question', 'Are you sure to delete this device?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.iotList.currentItem().state == 0:
                self.delete_question2()
            else:
                f = open("trusted", 'r')
                dataset = f.read()
                f.close()

                f = open("trusted", 'w')
                f.close()

                f = open("trusted", 'a')
                itemList = dataset.split('\n')
                for i in itemList:
                    if self.iotList.currentItem().text().split(" ")[3] not in i:
                        f.write(i + "\n")
                f.close()

                mac = self.iotList.currentItem().host.mac_address
                if mac in Whitelist.get_instance().semiwhitelist:
                    Whitelist.get_instance().remove_semiwhitelisted(mac)

                self.iotList.takeItem(self.iotList.currentRow())

    def delete_question2(self):
        reply = QMessageBox.question(self, 'question', 'This device is unconfirmed.\r\nDo you want to report?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.delete_report()
        self.iotList.takeItem(self.iotList.currentRow())

    def delete_report(self):
        QMessageBox.information(self, 'information', 'Reported.', QMessageBox.Ok)

    ## rename button
    def rename_Click(self):
        if (self.iotList.currentItem().state == 1) or (self.iotList.currentItem().state == 2):
            self.rename_edit()
        else:
            self.rename_warning()

    def rename_warning(self):
        QMessageBox.warning(self, 'Warning', 'This device is unconfirmed.\r\nPlease check first.', QMessageBox.Ok)

    def rename_edit(self):
        text, ok = QInputDialog.getText(self, 'Input Name', 'Enter new name:')
        st = self.iotList.currentItem().text().split("\r\n")
        self.iotList.currentItem().setText(st[0] + "\r\n" + str(text) + "\r\n")
        if ok:
            f = open("trusted", 'r')
            find = f.read()
            f.close()

            f = open("trusted", 'w')
            f.close()

            f = open("trusted", 'a')
            itemList = find.split('\n')
            for i in itemList:
                if self.iotList.currentItem().text().split(" ")[3] in i:
                    temp = i.split("=")
                    f.write(temp[0] + "=" + str(text) + "\n")
                else:
                    f.write(i + '\n')
            f.close()
    
    # history button
    def history_Click(self):
        history = HistoryGUI().__init__()

    ##scan button

    def scan_Click(self):
        self.scanbtn.setEnabled(False)
        print("Starting scan")
        self.scanner.scan_network_callback(lambda x: self.on_scan_completion(x), port_scan=True)

    def on_scan_completion(self, hosts):
        print("Scan completed")
        self.scanbtn.setEnabled(True)
        HistoryArchive.get_instance().add_scan(hosts)
        self.iotList.clear()
        i = 0

        whitelist = Whitelist.get_instance()

        for host in hosts:

            item = QListWidgetItem()
            item.state = 0
            item.host = host
            self.iotList.addItem(item)
            item = self.iotList.item(i)
            item_text_lines = [host.get_GUI_name(), "", "", ""]

            f = open("trusted", 'r')
            while True:
                line = f.readline()
                if not line: break
                if host.get_GUI_name().split(" ")[3] in line:
                    temp = line.split("=")
                    item_text_lines[1] = temp[len(temp)-1]
                    item.state = 1
            f.close()

            if len(host.ports) > 0:
                item_text_lines[2] = "  Ports: " + ", ".join((str(port.port_id) for port in host.ports))

            if host.mac_address in whitelist.semiwhitelist:
                allowed_ports = whitelist.semiwhitelist[host.mac_address]
                item.state = 2
                item.setIcon(QIcon('LocalNetworkGUI/safeicon.png'))
                item.setBackground(QColor(255, 240, 150))
                kick = False

                for port in host.ports:
                    port_str = str(port.port_id)
                    if port_str not in allowed_ports:
                        print("Device", host.get_GUI_name(), "has illegal port", port.port_id, "open!")
                        item_text_lines[3] = "    Illegal port {}. Deauthenticating from network...".format(port.port_id)
                        item_text_lines.append("")
                        kick = True
                if kick:
                    DeauthHandler.deauth_device(host, duration=20)
            elif item.state == 0:
                item.setIcon(QIcon('LocalNetworkGUI/dangericon.png'))
                item.setBackground(QColor(255, 195, 200))
            elif item.state == 1:
                item.setIcon(QIcon('LocalNetworkGUI/safeicon.png'))
                item.setBackground(QColor(200, 255, 200))
            else:
                item.setIcon(QIcon('LocalNetworkGUI/disconnecticon.png'))
                item.setBackground(QColor(200, 200, 200))
            item.setText("\r\n".join(item_text_lines))
            i += 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
