## 1. window

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from network.network_scanner import NetworkScanner

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
        scanbtn = QPushButton('Scan', self)
        scanbtn.setCheckable(False)
        scanbtn.move(20, 20)
        scanbtn.setIcon(QIcon('LocalNetworkGUI/scanicon.png'))
        scanbtn.resize(scanbtn.sizeHint())
        scanbtn.clicked.connect(self.scan_Click)
        scanbtn.toggle()

        ##Add Device Button
        addbtn = QPushButton('Add a device', self)
        addbtn.setCheckable(False)
        addbtn.move(165, 20)
        addbtn.setIcon(QIcon('LocalNetworkGUI/addicon.png'))
        addbtn.resize(addbtn.sizeHint())
        addbtn.clicked.connect(self.add_Click)
        addbtn.toggle()


        ##Delete Device Button
        deletebtn = QPushButton('Delete a device', self)
        deletebtn.setCheckable(False)
        deletebtn.move(336, 20)
        deletebtn.setIcon(QIcon('LocalNetworkGUI/deleteicon.png'))
        deletebtn.resize(deletebtn.sizeHint())
        deletebtn.clicked.connect(self.delete_Click)
        deletebtn.toggle()

        ##Rename Button
        renamebtn = QPushButton('Rename ', self)
        renamebtn.setCheckable(False)
        renamebtn.move(524, 20)
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
        historybtn.clicked.connect(QCoreApplication.instance().exit)
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


    ##scan button

    def scan_Click(self):
        print("Starting scan")
        self.scanner.scan_network_callback(lambda x: self.on_scan_completion(x))

    def on_scan_completion(self, hosts):
        print("Scan completed")
        self.iotList.clear()
        i = 0

        for host in hosts:

            item = QListWidgetItem()
            item.state = 0
            self.iotList.addItem(item)
            item = self.iotList.item(i)
            item.setText(host.get_GUI_name() + "\r\n\r\n")

            f = open("trusted", 'r')
            while True:
                line = f.readline()
                if not line: break
                if host.get_GUI_name().split(" ")[3] in line:
                    temp = line.split("=")
                    item.setText(host.get_GUI_name() + "\r\n" + temp[len(temp)-1])
                    item.state = 1
            f.close()

            if item.state == 0:
                item.setIcon(QIcon('LocalNetworkGUI/dangericon.png'))
                item.setBackground(QColor(255, 195, 200))
            elif item.state == 1:
                item.setIcon(QIcon('LocalNetworkGUI/safeicon.png'))
                item.setBackground(QColor(200, 255, 200))
            else:
                item.setIcon(QIcon('LocalNetworkGUI/disconnecticon.png'))
                item.setBackground(QColor(200, 200, 200))
            i += 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
