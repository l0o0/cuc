from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui



class MENU(QtWidgets.QWidget):
    def __init__(self, parent=None):
        #super(MENU, self).__init__(parent)
        self.setWindowTitle('Preference')
        self.width = 600
        self.height = 500
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setFixedSize(self.width, self.height)
        self.layout = QtWidgets.QVBoxLayout()
        self.tabs = QtWidgets.QTabWidget()    
        self.initTab1()
        self.initTab2()
        self.initTab3()
        self.tabs.addTab(self.tab1, "General")
        self.tabs.addTab(self.tab2, 'Task')
        self.tabs.addTab(self.tab3, "About")

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bb = QtWidgets.QDialogButtonBox()
        self.bb.setGeometry(QtCore.QRect(150, 250, 341, 32))
        self.bb.setOrientation(QtCore.Qt.Horizontal)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.button(QtWidgets.QDialogButtonBox.Cancel).setToolTip('Discard changes and close the menu')
        self.bb.button(QtWidgets.QDialogButtonBox.Ok).setToolTip('Save changes')
        self.bb.accepted.connect(self.accept)
        self.bb.rejected.connect(self.reject)
        self.bottom_layout.addWidget(self.bb)

        self.layout.addWidget(self.tabs)
        self.layout.addLayout(self.bottom_layout)
        self.setLayout(self.layout)
        # show menu in center screen
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.setGeometry(*(centerPoint.x() - self.width * 0.5, 
                            centerPoint.y() - self.height * 0.5,
                            self.width,
                            self.height))

    
    def initTab1(self):
        self.tab1 = QtWidgets.QWidget()
        self.tab1.layout = QtWidgets.QGridLayout()
        self.tab1.layout.setAlignment(QtCore.Qt.AlignTop)

        self.tab1groupBox1 = QtWidgets.QGroupBox('Todo File')
        self.tab1groupBox1.setMaximumHeight(100)
        self.tab1groupBox1Layout = QtWidgets.QGridLayout()
        self.createLabel(self.tab1groupBox1Layout, 'TODO', 50, 0, 0)
        self.createLabel(self.tab1groupBox1Layout, 'DONE', 50, 1, 0)
        self.todotxt = QtWidgets.QLineEdit('todo.txt')
        self.donetxt = QtWidgets.QLineEdit('done.txt')
        self.todoButton = self.createBroswerButton()
        self.doneButton = self.createBroswerButton()
        self.todoButton.clicked.connect(self.openFileDialog)
        self.doneButton.clicked.connect(self.openFileDialog)
        self.tab1groupBox1Layout.addWidget(self.todotxt, 0, 1)
        self.tab1groupBox1Layout.addWidget(self.donetxt, 1, 1)
        self.tab1groupBox1Layout.addWidget(self.todoButton, 0, 2)
        self.tab1groupBox1Layout.addWidget(self.doneButton, 1, 2)
        self.tab1groupBox1.setLayout(self.tab1groupBox1Layout)
        self.tab1.layout.addWidget(self.tab1groupBox1, 0, 0)

        self.tab1groupBox2 = QtWidgets.QGroupBox('Window Layout')
        self.tab1groupBox2.setMaximumHeight(100)
        self.tab1groupBox2Layout = QtWidgets.QVBoxLayout()
        self.sepWinButton = QtWidgets.QCheckBox("Get rid of the taskbar.")
        self.sepWinButton.checked = False
        lb = QtWidgets.QLabel('Opacity')
        lb.setMaximumWidth(50)
        self.tab1groupBox2Layout.addWidget(self.sepWinButton)
        self.tab1groupBox2Layout.addWidget(lb)
        self.tab1groupBox2.setLayout(self.tab1groupBox2Layout)
        self.tab1.layout.addWidget(self.tab1groupBox2, 1,0)

        self.tab1groupBox3 = QtWidgets.QGroupBox('Global Shortcuts')
        self.tab1groupBox3.setMaximumHeight(100)
        self.tab1groupBox3Layout = QtWidgets.QGridLayout()
        self.createLabel(self.tab1groupBox3Layout, 'Show Window', 90, 0, 0)
        self.createLabel(self.tab1groupBox3Layout, "Stay on Top", 90, 1, 0)
        self.showWin = QtWidgets.QLineEdit()
        self.keepTop = QtWidgets.QLineEdit()
        self.tab1groupBox3Layout.addWidget(self.showWin, 0, 1)
        self.tab1groupBox3Layout.addWidget(self.keepTop, 1,1)
        self.tab1groupBox3.setLayout(self.tab1groupBox3Layout)
        self.tab1.layout.addWidget(self.tab1groupBox3)

        self.tab1.setLayout(self.tab1.layout)    


    def initTab2(self):
        self.tab2 = QtWidgets.QWidget()
        self.tab2.layout = QtWidgets.QGridLayout()
        self.tab2.layout.setAlignment(QtCore.Qt.AlignTop)

        self.tab2groupBox1 = QtWidgets.QGroupBox("Task Style")
        self.tab2groupBox1Layout = QtWidgets.QGridLayout()
        self.tab2groupBox1Layout.setAlignment(QtCore.Qt.AlignLeft)

        self.createLabel(self.tab2groupBox1Layout, 'Priority', 100, 0, 0)
        self.createLabel(self.tab2groupBox1Layout, 'Complete Date', 100, 1, 0)
        self.createLabel(self.tab2groupBox1Layout, 'Create Date', 100, 2, 0)
        self.createLabel(self.tab2groupBox1Layout, 'Content', 100, 3, 0)
        self.createLabel(self.tab2groupBox1Layout, 'Project', 100, 4, 0)
        self.createLabel(self.tab2groupBox1Layout, 'Key:Value', 100, 5, 0)

        self.createLineEdit(self.tab2groupBox1Layout, 'Priority', 100, 0, 1)
        self.createLineEdit(self.tab2groupBox1Layout, 'Complete Date', 100, 1, 1)
        self.createLineEdit(self.tab2groupBox1Layout, 'Create Date', 100, 2, 1)
        self.createLineEdit(self.tab2groupBox1Layout, 'Content', 100, 3, 1)
        self.createLineEdit(self.tab2groupBox1Layout, 'Project', 100, 4, 1)
        self.createLineEdit(self.tab2groupBox1Layout, 'Key:Value', 100, 5, 1)

        for i in range(6):
            self.createColorButton(i)

        self.tab2groupBox1.setLayout(self.tab2groupBox1Layout)
        self.tab2.layout.addWidget(self.tab2groupBox1)
        self.tab2.setLayout(self.tab2.layout)


    def initTab3(self):
        self.tab3 = QtWidgets.QWidget()
        self.tab3.layout = QtWidgets.QVBoxLayout()
        self.tab3.layout.setAlignment(QtCore.Qt.AlignTop)
        lb = QtWidgets.QLabel()
        lb.setText('About')
        self.tab3.layout.addWidget(lb)
        self.tab3.setLayout(self.tab3.layout)
    

    def createBroswerButton(self):
        butt = QtWidgets.QPushButton('Broswer')
        butt.setMaximumWidth(80)
        return butt


    def createColorButton(self, row, color='green'):
        butt = QtWidgets.QPushButton()
        butt.setMaximumWidth(30)
        butt.setStyleSheet("background-color: %s" % color)
        butt.clicked.connect(self.openColorDialog)
        self.tab2groupBox1Layout.addWidget(butt, row, 2)


    def createLabel(self, layout, text, width, row, col):
        label = QtWidgets.QLabel(text)
        label.setMaximumWidth(width)
        layout.addWidget(label, row, col)


    def createLineEdit(self, layout, text, width, row, col):
        le = QtWidgets.QLineEdit(text)
        le.setMaximumWidth(width)
        layout.addWidget(le, row, col)


    def openFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select File", "","All Files (*);;Txt file (*.txt)", options=options)
        if fileName:
            print(fileName)


    def openColorDialog(self):
        button = self.sender()
        print(self.tab2groupBox1Layout.indexOf(button))
        try:
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                print(color.name())
        except:
            print("ERROR")

    
    def accept(self):
        # new changes should take effect.
        print('accept')  


    def reject(self):
        print('reject & close')
        self.close()

