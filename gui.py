import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDesktopWidget, QLineEdit, \
                            QSystemTrayIcon, QMenu, QAction, QTabWidget, QVBoxLayout, \
                            QPushButton, QTableWidget, QHeaderView, QMessageBox, \
                            QGridLayout, QPushButton, QTableWidgetItem, \
                            QAbstractItemView, QHBoxLayout, QLayout
from PyQt5.QtGui import QIcon, QPixmap, QDropEvent
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from pyqtkeybind import keybinder 

from task import Tasks, TaskLine
from tab1 import TAB1



class WinEventFilter(QtCore.QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0



class App(QWidget):

    def __init__(self, tab1):
        super().__init__()
        self.title = 'Keep Going'
        self.left = 10
        self.top = 10
        self.width = 450
        self.height = 360
        self.initUI()
        self.tab1 = tab1
        self.tab2()
        self.tab3()
        self.initTab()
        

        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        # 设置窗口固定大小
        self.setFixedSize(self.width, self.height)
        # 设置窗体无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        # 设置透明背景
        #self.setWindowOpacity(0.85)

        ag = QDesktopWidget().availableGeometry()    # 显示器可用的长宽信息
        self.fixedGeometry = (ag.width() - self.width - 20, 
                        ag.height() - self.height - 5, 
                        self.width, 
                        self.height)
        self.setGeometry(*self.fixedGeometry)
        self.show()


    def initTab(self):
        # init tab 
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()       
        self.tabs.resize(478, 358)
        self.tabs.addTab(self.tab1, "TODO")
        self.tabs.addTab(self.tab2, 'DONE')
        self.tabs.addTab(self.tab3, "Summary")
        self.bottom = QHBoxLayout()
        self.pinButton = QtWidgets.QPushButton()
        self.menuButton = QtWidgets.QPushButton()
        self.pinButton.setMaximumSize(30, 30)
        self.pinButton.setCheckable(True)
        self.pinButton.setIcon(QtGui.QIcon("icons/pinterest2.png"))
        self.pinButton.clicked.connect(self.winPinTop)
        self.menuButton = QPushButton()
        self.menuButton.setMaximumSize(30, 30)
        self.menuButton.setChecked(True)
        self.menuButton.setIcon(QtGui.QIcon("icons/cog.png"))
        self.bottom.addWidget(self.pinButton,alignment=QtCore.Qt.AlignRight)
        self.bottom.addWidget(self.menuButton)
        self.bottom.setContentsMargins(1, 1, 1, 1)

        # add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.bottom)
        self.layout.setContentsMargins(0, 1, 0, 2)
        self.setLayout(self.layout)

        # tab1 
    

        # tab2 
    def tab2(self):
        self.tab2 = QWidget()
        self.tab2.layout = QVBoxLayout()
        lb = QLabel()
        lb.setText('Done')
        self.tab2.layout.addWidget(lb)
        self.tab2.setLayout(self.tab2.layout)

    
    # tab3 
    def tab3(self):
        self.tab3 = QWidget()
        self.tab3.layout = QVBoxLayout()
        lb = QLabel()
        lb.setText('Summary')
        self.tab3.layout.addWidget(lb)
        self.tab3.setLayout(self.tab3.layout)

    # hide to system tray instead of close
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    # display window in the right bottom
    def rightBottomShow(self):
        self.setGeometry(*self.fixedGeometry)
        self.show()

    
    def shortcut(self):
        print('press shortcut')
        if self.isHidden():
            self.rightBottomShow()
        else:
            self.hide()
    
    

    @QtCore.pyqtSlot()
    def winPinTop(self):
        button = self.sender()
        if button.isChecked():
            print('on top')
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint| QtCore.Qt.Tool)
            self.rightBottomShow()
        else:
            print('no top')
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint |QtCore.Qt.Tool)
            self.rightBottomShow()



class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        menu = QMenu(parent)
        showAction = menu.addAction('Show')
        showAction.triggered.connect(parent.rightBottomShow)
        menu.addSeparator()
        exitAction = menu.addAction('Exit')
        exitAction.triggered.connect(self.exit)      
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)


    def exit(self):
        self.parent.tab1.tasks.saveToFile()
        QtCore.QCoreApplication.exit()        


    def onTrayIconActivated(self, reason):
        #print(reason, '--reason--')
        if reason == QSystemTrayIcon.Trigger:
            #print(self.parent.frameGeometry(), self.parent.normalGeometry(), ag, sg)
            if self.parent.isHidden():
                self.parent.rightBottomShow()
            else:
                self.parent.hide()



if __name__ == '__main__':
    config = {'todotxt':'todo.txt',
            'donetxt':'done.txt'}
    tasks = Tasks(config['todotxt'], config['donetxt'])
    tasks.readFromFile()

    app = QApplication(sys.argv)
    tab1 = TAB1(tasks)
    ex = App(tab1)
    trayIcon = SystemTrayIcon(QIcon("icons/icon.png"), ex)
    trayIcon.show()

    # keybinder from here
    keybinder.init()
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QtCore.QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)
    keybinder.register_hotkey(ex.winId(), "Shift+Ctrl+A", ex.shortcut)
    keybinder.register_hotkey(tab1.winId(), "Shift+Ctrl+B", tab1.testbutton)

    sys.exit(app.exec_())
    keybinder.unregister_hotkey(ex.winId(), "Shift+Ctrl+A")


