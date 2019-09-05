from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui 
from task import TaskLine


class HiddenLabel(QtWidgets.QLabel):
    '''
    QLable hide when mouse pressed
    '''
    def __init__(self, buddy, taskline, parent = None):
        super().__init__()
        #self.setFixedHeight(50)
        self.buddy = buddy
        self.taskline = taskline
        self.setText(self.taskline.enrich_text())

    # left double clicked to edit
    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.hide()
            print('double click', self.taskline.plain_text)
            self.buddy.setText(self.taskline.plain_text)
            self.buddy.show()
            self.buddy.setFocus()



class EditableCell(QtWidgets.QWidget):
    '''
    QLineEdit show when HiddenLabel is hidden
    '''
    def __init__(self, taskline, parent = None):
        super().__init__()
        self.taskline = taskline
        # Create ui
        self.myEdit = QtWidgets.QLineEdit()
        #self.myEdit.setFixedHeight(50)
        self.myEdit.hide() # Hide line edit
        self.myEdit.returnPressed.connect(self.textEdited)
        # Create our custom label, and assign myEdit as its buddy
        self.myLabel = HiddenLabel(self.myEdit, self.taskline) 
        

        # Put them under a layout together
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.myLabel)
        hLayout.addWidget(self.myEdit)
        hLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hLayout)


    def textEdited(self):
        # If the input is left empty, revert back to the label showing
        print('edit finished', self.myEdit.text())
        taskline = TaskLine()
        taskline.parser(self.myEdit.text())
        self.taskline = taskline
        print(self.taskline.plain_text)
        # update text after saving
        self.myLabel.setText(taskline.enrich_text())
        self.myLabel.taskline = self.taskline
        self.myEdit.hide()
        self.myLabel.show()
        self.myLabel.setFocus()



class TAB1(QtWidgets.QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.layout = QtWidgets.QGridLayout()
        self.layout.setVerticalSpacing(2)

        # add text edit line for new task
        self.textboxAdd = QtWidgets.QLineEdit()
        self.textboxAdd.setPlaceholderText('Input something ...')
        self.textboxAdd.setFixedHeight(25)
        self.textboxAdd.setFixedWidth(436)
        self.layout.addWidget(self.textboxAdd, 0, 0, 1, 10)
        self.textboxAdd.returnPressed.connect(self.addLine)

        # add layout for added tasks
        self.tab1TaskTable = QtWidgets.QTableWidget()
        self.tab1TaskTable.verticalHeader().setVisible(False)
        self.tab1TaskTable.horizontalHeader().setVisible(False)
        self.tab1TaskTable.setShowGrid(False)
        self.tab1TaskTable.setColumnCount(3)
        self.tab1TaskTable.setRowCount(len(self.tasks.tasklines))
        self.tab1TaskTable.setColumnWidth(0, 380)
        self.tab1TaskTable.setColumnWidth(1, 20)
        self.tab1TaskTable.setColumnWidth(2, 20)
        self.tab1TaskTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.layout.addWidget(self.tab1TaskTable, 1, 0, 15, 13)

        # add widget for menu button
        # self.tab1Pin = QtWidgets.QPushButton()
        # self.tab1Pin.setMaximumSize(30, 30)
        # self.tab1Pin.setCheckable(True)
        # self.tab1Pin.setIcon(QtGui.QIcon("icons/pinterest2.png"))
        # self.tab1Pin.clicked.connect(self.winPinTop)
        # self.tab1Menu = QPushButton()
        # self.tab1Menu.setMaximumSize(30, 30)
        # self.tab1Menu.setChecked(True)
        # self.tab1Menu.setIcon(QtGui.QIcon("icons/cog.png"))
        # self.layout.addWidget(self.tab1Pin,16, 9)
        # self.layout.addWidget(self.tab1Menu,16, 10)
        # display tasks
        for i, t in enumerate(self.tasks.tasklines):
            print('init row %s' % i)
            cellwidget = self.createCellQlabel(t)
            self.tab1TaskTable.setCellWidget(i, 0, cellwidget)
            editButton = self.createButton('checkmark')
            deleteButton = self.createButton('delete')            
            self.tab1TaskTable.setCellWidget(i,1, editButton)
            self.tab1TaskTable.setCellWidget(i,2, deleteButton)
        print('init table rows ', self.tab1TaskTable.rowCount())
        self.layout.setContentsMargins(3,3,3,0)
        self.setLayout(self.layout)


    # create button in taskline
    def createButton(self, t):
        self.butt = QtWidgets.QPushButton()
        self.butt.setMaximumSize(25, 25)
        if t == 'delete':
            self.butt.setIcon(QtGui.QIcon("icons/cancel-circle.png"))      
            self.butt.clicked.connect(self.deleteButtonAction)     
        elif t == 'checkmark':
            self.butt.setIcon(QtGui.QIcon("icons/checkmark.png"))
            self.butt.clicked.connect(self.checkButtonAction)
        return self.butt


    # create editable cell
    def createCellQlabel(self, taskline):
        cellwidget = EditableCell(taskline) 
        return cellwidget       


    def addLine(self):
        #QMessageBox.information(self, "Info", "Enter Pressed.")
        print('total rows before', self.tab1TaskTable.rowCount())
        if not self.textboxAdd.text().strip():
            QtWidgetss.QMessageBox.information(self, "Info", "Input something")
        else:
            rowidx = 0
            self.tab1TaskTable.insertRow(rowidx)
            taskline = TaskLine()
            taskline.parser(self.textboxAdd.text())
            cellwidget = self.createCellQlabel(taskline)
            self.tab1TaskTable.setCellWidget(rowidx, 0, cellwidget)
            editButton = self.createButton('checkmark')
            deleteButton = self.createButton('delete')
            self.tab1TaskTable.setCellWidget(rowidx, 1, editButton)
            self.tab1TaskTable.setCellWidget(rowidx, 2, deleteButton)
            self.textboxAdd.clear()
            self.tasks.tasklines.insert(0, taskline)
        print('total rows after', self.tab1TaskTable.rowCount())


    def checkButtonAction(self):
        button = self.sender()
        if button:
            row = self.tab1TaskTable.indexAt(button.pos()).row()
            self.checkcellwidget = self.tab1TaskTable.cellWidget(row, 0)
            completion_date = datetime.now().strftime('%Y-%m-%d')
            self.checkcellwidget.taskline.completion_date = completion_date
            self.checkcellwidget.taskline.mask = 'x'
            print(self.checkcellwidget.taskline.format_text())
            print('check ', row, self.tasks.tasklines[row].plain_text)
            self.tasks.saveDoneTask(self.checkcellwidget.taskline)
            self.tab1TaskTable.removeRow(row)
            del self.tasks.tasklines[row]


    
    def deleteButtonAction(self):
        button = self.sender()
        if button:
            row = self.tab1TaskTable.indexAt(button.pos()).row()
            #column = self.tab1TaskTable.column(button)
            self.tab1TaskTable.removeRow(row)
            del self.tasks.tasklines[row]
        print('delete', row)
