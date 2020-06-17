## 2. window

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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

        ##window
        self.setWindowTitle("History")
        self.setGeometry(400, 100, 801, 420)
        self.show()

if __name__ == '__main__':
    app2 = QApplication(sys.argv)
    dialog = HistoryGUI()
    sys.exit(app2.exec_())
