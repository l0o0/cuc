import sys
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QVBoxLayout, QPushButton, QPushButton
from PyQt5 import QtCore

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Keep Going'
        self.width = 480
        self.height = 360
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        win = QWidget()        
        win.setFixedSize(self.width, self.height)
        layout = QVBoxLayout()
        button = QPushButton('PinTop')
        button.setCheckable(True)
        button.clicked.connect(self.winPinTop)
        layout.addWidget(button)
        # add tabs to widget
        win.setLayout(layout)
        self.setCentralWidget(win)
        self.show()

    
    def winPinTop(self):
        print('Pin')
        button = self.sender()
        if button.isChecked():
            print('on top')
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

            print(self.windowFlags())
            self.show()
        else:
            print('no top')
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            print(self.windowFlags())
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())