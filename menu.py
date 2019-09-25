from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui



class MENU(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MENU, self).__init__(parent)
        self.setWindowTitle('Preference')
        self.width = 600
        self.height = 500
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
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
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.RestoreDefaults | QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.button(QtWidgets.QDialogButtonBox.Cancel).setToolTip('Discard changes and close the menu')
        self.bb.button(QtWidgets.QDialogButtonBox.Ok).setToolTip('Save changes')
        self.bb.accepted.connect(self.accept)
        self.bb.rejected.connect(self.reject)
        self.bb.clicked.connect(self.restoreDefaults)
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
        self.todotxt = QtWidgets.QLineEdit(self.parent().config.config['todotxt'])
        self.donetxt = QtWidgets.QLineEdit(self.parent().config.config['donetxt'])
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
        self.tab1groupBox2Layout = QtWidgets.QGridLayout()
        self.sepWinButton = QtWidgets.QCheckBox("Get rid of the taskbar.")
        self.sepWinButton.checked = False
        lb = QtWidgets.QLabel('Opacity')
        lb.setMaximumWidth(50)
        self.opacitySlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacitySlider.setMinimum(0)
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setMaximumWidth(300)
        self.opacitySlider.setValue(self.parent().config.config['layout']['window_opacity']*100)
        self.opacitySlider.setSingleStep(1)
        self.opacityLabel = QtWidgets.QLabel(str(self.opacitySlider.value()/100))
        self.opacitySlider.valueChanged.connect(self.changeOpacity)
        self.tab1groupBox2Layout.addWidget(self.sepWinButton, 0, 0)
        self.tab1groupBox2Layout.addWidget(lb, 1,0)
        self.tab1groupBox2Layout.addWidget(self.opacitySlider, 1, 1 )
        self.tab1groupBox2Layout.addWidget(self.opacityLabel, 1, 2)
        self.tab1groupBox2.setLayout(self.tab1groupBox2Layout)
        self.tab1.layout.addWidget(self.tab1groupBox2, 1,0)

        self.tab1groupBox3 = QtWidgets.QGroupBox('Global Shortcuts')
        self.tab1groupBox3.setMaximumHeight(100)
        self.tab1groupBox3Layout = QtWidgets.QGridLayout()
        self.tab1groupBox3Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.createLabel(self.tab1groupBox3Layout, 'Show Window', 90, 0, 0)
        self.createLabel(self.tab1groupBox3Layout, "Stay on Top", 90, 1, 0)
        self.showWin = QtWidgets.QLineEdit(self.parent().config.config['hotkey']['display'])
        self.showWin.setMaximumWidth(200)
        self.keepTop = QtWidgets.QLineEdit(self.parent().config.config['hotkey']['pin'])
        self.keepTop.setMaximumWidth(200)
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

        istart = 0
        for k1 in self.parent().config.config['style'].keys():
            tmp = self.parent().config.config['style'][k1]
            if isinstance(tmp, dict):
                for k2 in tmp.keys():
                    self.createLabel(self.tab2groupBox1Layout, '%s:%s' % (k1, k2), 100, istart%6, 0 + (istart//6)*3)
                    self.createLineEdit(self.tab2groupBox1Layout, tmp[k2], 100, istart%6, 1 + (istart//6)*3)
                    self.createColorButton(istart%6, 2 + (istart//6)*3, tmp[k2])
                    istart += 1
            else:
                self.createLabel(self.tab2groupBox1Layout, '%s' % k1, 100, istart%6, 0+ (istart//6)*3)
                self.createLineEdit(self.tab2groupBox1Layout, tmp, 100, istart%6, 1+ (istart//6)*3)
                self.createColorButton(istart%6, 2+ (istart//6)*3, tmp)
                istart += 1

        self.tab2groupBox2 = QtWidgets.QGroupBox("Task Font Size")
        self.tab2groupBox2.setMaximumHeight(80)
        self.tab2groupBox2Layout = QtWidgets.QGridLayout()
        self.tab2groupBox2Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.createLabel(self.tab2groupBox2Layout, 'Font Size', 80, 0, 0)
        self.fontsizeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.fontsizeSlider.setMaximum(20)
        self.fontsizeSlider.setMinimum(10)
        self.fontsizeSlider.setMaximumWidth(300)
        self.fontsizeSlider.setSingleStep(1)
        self.fontsizeSlider.setValue(self.parent().config.config['fontsize'])
        self.fontsizeSlider.valueChanged.connect(self.changeFontSize)
        self.tab2groupBox2Layout.addWidget(self.fontsizeSlider, 0, 1)
        self.fontsize = QtWidgets.QLabel(str(self.parent().config.config['fontsize']))
        #self.fontsize.setMaximumWidth(35)
        self.fontsize.setMaximumSize(35, 35)
        self.tab2groupBox2Layout.addWidget(self.fontsize, 0, 2)
        self.test_text = QtWidgets.QLabel("A字体")
        self.test_text.setMinimumHeight(40)
        self.test_text.setStyleSheet("QLabel{font-size:%spx}" % self.parent().config.config['fontsize'])
        self.tab2groupBox2Layout.addWidget(self.test_text, 0, 3)

        self.tab2groupBox1.setLayout(self.tab2groupBox1Layout)
        self.tab2groupBox2.setLayout(self.tab2groupBox2Layout)
        self.tab2.layout.addWidget(self.tab2groupBox1)
        self.tab2.layout.addWidget(self.tab2groupBox2)
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


    def createColorButton(self, row, col, color='green'):
        butt = QtWidgets.QPushButton()
        butt.setMaximumWidth(30)
        butt.setStyleSheet("background-color: %s" % color)
        #butt.clicked.connect(self.openColorDialog)
        self.tab2groupBox1Layout.addWidget(butt, row, col)


    def createLabel(self, layout, text, width, row, col):
        label = QtWidgets.QLabel(text)
        label.setMaximumWidth(width)
        layout.addWidget(label, row, col)


    def createLineEdit(self, layout, text, width, row, col):
        le = QtWidgets.QLineEdit(text)
        le.setMaximumWidth(width)
        layout.addWidget(le, row, col)


    def openFileDialog(self):
        idx = self.tab1groupBox1Layout.indexOf(self.sender())
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Select File", "","All Files (*);;Txt file (*.txt)", options=options)
        if fileName:
            if idx == 4:
                self.todotxt.setText(fileName)
            elif idx == 5:
                self.donetxt.setText(fileName)

    def changeFontSize(self):
        self.fontsize.setText(str(self.fontsizeSlider.value()))
        self.test_text.setStyleSheet("QLabel{font-size:%spx}" % self.fontsizeSlider.value())

    def changeOpacity(self):
        self.opacityLabel.setText(str(self.opacitySlider.value()/100))


    # todo
    def saveConfig(self):
        tmp_config = self.parent().config.config
        tmp_config['todotxt'] = self.todotxt.text()
        tmp_config['donetxt'] = self.donetxt.text()
        tmp_config['layout']['window_fixed'] = self.sepWinButton.checked
        tmp_config['layout']['window_opacity'] = self.opacitySlider.value()
        tmp_config['hotkey']['pin'] = self.keepTop.text()
        tmp_config['hotkey']['display'] = self.showWin.text()
        tmp_config['fontsize'] = int(self.fontsize.text())
        tmp_config['style']['priority']['(A)'] = self.tab2groupBox1Layout.itemAt(1).widget().text()
        tmp_config['style']['priority']['(B)'] = self.tab2groupBox1Layout.itemAt(4).widget().text()
        tmp_config['style']['priority']['(C)'] = self.tab2groupBox1Layout.itemAt(7).widget().text()
        tmp_config['style']['priority']['(D)'] = self.tab2groupBox1Layout.itemAt(10).widget().text()
        tmp_config['style']['completion_date'] = self.tab2groupBox1Layout.itemAt(13).widget().text()
        tmp_config['style']['creation_date'] = self.tab2groupBox1Layout.itemAt(16).widget().text()
        tmp_config['style']['content'] = self.tab2groupBox1Layout.itemAt(19).widget().text()
        tmp_config['style']['project'] = self.tab2groupBox1Layout.itemAt(22).widget().text()
        tmp_config['style']['context'] = self.tab2groupBox1Layout.itemAt(25).widget().text()
        tmp_config['style']['keyvalue']['k'] = self.tab2groupBox1Layout.itemAt(28).widget().text()
        tmp_config['style']['keyvalue']['v'] = self.tab2groupBox1Layout.itemAt(31).widget().text()
        #print(tmp_config)

    # def openColorDialog(self):
    #     button = self.sender()
    #     print(self.tab2groupBox1Layout.indexOf(button))
    #     try:
    #         color = QtWidgets.QColorDialog.getColor()
    #         if color.isValid():
    #             print(color.name())
    #     except:
    #         print("ERROR")
    
    # override parent close event
    def closeEvent(self, event):
        #event.ignore()
        self.close()
    
    def accept(self):
        # new changes should take effect.
        print('accept')  
        self.saveConfig()

    def reject(self):
        self.close()

    def restoreDefaults(self):
        print('restore')

