## 1. window

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.datetime = QDateTime.currentDateTime()
        self.initUI()

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

        ##item list
        _translate = QCoreApplication.translate
        i = 0
        for i in range(20):
            item = QListWidgetItem()
            item.state = 0
            self.iotList.addItem(item)
            item = self.iotList.item(i)
            item.setText(_translate("iotList", " Device " + str(i + 1) + "\r\n\r\n"))
            if item.state == 0:
                item.setIcon(QIcon('dangericon.png'))
                item.setBackground(QColor(255, 195, 200))
            elif item.state == 1:
                item.setIcon(QIcon('safeicon.png'))
                item.setBackground(QColor(200, 255, 200))
            else:
                item.setIcon(QIcon('disconnecticon.png'))
                item.setBackground(QColor(200, 200, 200))


        ##Scan Button
        scanbtn = QPushButton('Scan', self)
        scanbtn.setCheckable(False)
        scanbtn.move(20, 20)
        scanbtn.setIcon(QIcon('scanicon.png'))
        scanbtn.resize(scanbtn.sizeHint())
        scanbtn.clicked.connect(self.scan_Click)
        scanbtn.toggle()

        ##Add Device Button
        addbtn = QPushButton('Add a device', self)
        addbtn.setCheckable(False)
        addbtn.move(165, 20)
        addbtn.setIcon(QIcon('addicon.png'))
        addbtn.resize(addbtn.sizeHint())
        addbtn.clicked.connect(self.add_Click)
        addbtn.toggle()


        ##Delete Device Button
        deletebtn = QPushButton('Delete a device', self)
        deletebtn.setCheckable(False)
        deletebtn.move(336, 20)
        deletebtn.setIcon(QIcon('deleteicon.png'))
        deletebtn.resize(deletebtn.sizeHint())
        deletebtn.clicked.connect(self.delete_Click)
        deletebtn.toggle()

        ##Rename Button
        renamebtn = QPushButton('Rename ', self)
        renamebtn.setCheckable(False)
        renamebtn.move(524, 20)
        renamebtn.setIcon(QIcon('renameicon.png'))
        renamebtn.resize(renamebtn.sizeHint())
        renamebtn.clicked.connect(self.rename_Click)
        renamebtn.toggle()

        ##History Device Button
        historybtn = QPushButton('History', self)
        historybtn.setCheckable(False)
        historybtn.move(670, 20)
        historybtn.setIcon(QIcon('historyicon.png'))
        historybtn.resize(historybtn.sizeHint())
        #historybtn.setStyleSheet('background: red;')
        historybtn.clicked.connect(QCoreApplication.instance().exit)
        historybtn.toggle()

        ##Risk Label
        risk = QLabel(self)
        risk.resize(50, 50)
        pixmap = QPixmap("riskicon.png")
        pixmap = pixmap.scaledToWidth(30)
        risk.setPixmap(QPixmap(pixmap))
        risk.move(640, 15)
        risk.hide()

        ##window
        self.setWindowTitle("Home IoT security")
        self.setWindowIcon(QIcon('homeicon.png'))
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
            self.iotList.currentItem().setIcon(QIcon('safeicon.png'))
            self.iotList.currentItem().setBackground(QColor(200, 255, 200))
            item = self.iotList.takeItem(self.iotList.currentRow())
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
        if ok:
            self.iotList.currentItem().setText(' ' + str(text) + '\r\n\r\n')

    ##scan button
    def scan_Click(self):
        print("Hi")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())