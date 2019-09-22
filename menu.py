from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui



class MENU(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MENU, self).__init__(parent)
        self.width = 600
        self.height = 500
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setFixedSize(self.width, self.height)
        self.layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()    
        self.initTab1()
        self.initTab2()
        self.initTab3()
        self.tabs.addTab(self.tab1, "Layout")
        self.tabs.addTab(self.tab2, 'Task')
        self.tabs.addTab(self.tab3, "HotKey")

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.discard = QtWidgets.QPushButton()
        self.save = QtWidgets.QPushButton()
        self.discard.setMaximumSize(30, 30)
        self.discard.setCheckable(True)
        self.discard.setIcon(QtGui.QIcon("icons/cross.png"))
        #self.discard.clicked.connect(self.winPinTop)
        self.save = QtWidgets.QPushButton()
        self.save.setMaximumSize(30, 30)
        self.save.setChecked(True)
        self.save.setIcon(QtGui.QIcon("icons/checkmark.png"))
        #self.save.clicked.connect(self.showMenu)
        self.bottom_layout.addWidget(self.discard,alignment=QtCore.Qt.AlignRight)
        self.bottom_layout.addWidget(self.save)
        self.bottom_layout.setContentsMargins(1, 1, 1, 1)

        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.bottom_layout)
        self.setLayout(self.layout)
        # show menu in center screen
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.setGeometry(*(centerPoint.x() - self.width * 0.5, 
                            centerPoint.y() - self.height * 0.5,
                            self.width,
                            self.height))

        QtGui.QFontDatabase.addApplicationFont('NotoColorEmoji.ttf')

    
    def initTab1(self):
        self.tab1 = QtWidgets.QWidget()
        self.tab1.layout = QtWidgets.QVBoxLayout()
        lb = QtWidgets.QLabel()
        lb.setText('Layout')
        self.tab1.layout.addWidget(lb)
        self.tab1.setLayout(self.tab1.layout)
    

    def initTab2(self):
        self.tab2 = QtWidgets.QWidget()
        self.tab2.layout = QtWidgets.QVBoxLayout()
        lb = QtWidgets.QLabel()
        lb.setFont(QtGui.QFont('NotoColorEmoji'))
        lb.setText(u"I'm a happy \U0001F600")
        self.tab2.layout.addWidget(lb)
        self.tab2.setLayout(self.tab2.layout)


    def initTab3(self):
        self.tab3 = QtWidgets.QWidget()
        self.tab3.layout = QtWidgets.QVBoxLayout()
        lb = QtWidgets.QLabel()
        lb.setText('HotKey')
        self.tab3.layout.addWidget(lb)
        self.tab3.setLayout(self.tab3.layout)
