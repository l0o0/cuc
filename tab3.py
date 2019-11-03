from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui 
from task import TaskLine


class TaskCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super(TaskCalendar, self).__init__(parent)
        self.setLocale(QtCore.QLocale('zh_CN'))
    
    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        # print(self.parent().parent().widget(1)) # this is tab2 
        tmp = self.parent().parent().widget(1).doneTasks.tasklines
        donetasks = [t for t in tmp if t.completion_date == date]
        createtasks = [t for t in tmp if t.creation_date == date]
        painter.setPen(QtCore.Qt.NoPen)

        if len(createtasks) > 0:
            c = QtGui.QColor("#FFA500")
            d = len(createtasks) // 2
            painter.setBrush(QtGui.QColor.darker(c, 100*(1 + 4 if d >4 else d)))
            painter.drawEllipse(rect.topLeft() + QtCore.QPoint(12, 10), 6, 6)
        if len(donetasks) > 0:
            c = QtGui.QColor("#c6e48b")
            d = len(donetasks) // 2
            painter.setBrush(QtGui.QColor.darker(c, 100*(1 + 4 if d >4 else d)))
            painter.drawEllipse(rect.topRight() + QtCore.QPoint(-12, 10), 6, 6)

        

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print('double click')
            # self.buddy.setFocus()
            

class TAB3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TAB3, self).__init__(parent)
        self.config = self.parent().config
        self.initCal()
        
    def initCal(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.cal = TaskCalendar(self)
        self.cal.setGridVisible(True)
        self.cal.clicked[QtCore.QDate].connect(self.showDate)
        self.cal.activated.connect(self.showTasks)
        self.layout.addWidget(self.cal)
        # task summary bar at buttom
        self.label = QtWidgets.QLabel("Click to see!")
        self.label.setFixedHeight(15)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
    

    def showDate(self, date):
        tmp = self.parent().parent().widget(1).doneTasks.tasklines
        donetasks = [t for t in tmp if t.completion_date == date]
        createtasks = [t for t in tmp if t.creation_date == date]
        self.label.setText("%s, create tasks: %s, done tasks: %s" % (date.toString(QtCore.Qt.ISODate), len(createtasks), len(donetasks)))
    

    def showTasks(self, date):
        tmp = self.parent().parent().widget(1).doneTasks.tasklines
        donetasks = [t for t in tmp if t.completion_date == date]
        createtasks = [t for t in tmp if t.creation_date == date]
        taskDialog = QtWidgets.QDialog(self)
        taskDialog.setWindowTitle('Task List')
        taskDialog.setMinimumWidth(412)
        layout = QtWidgets.QVBoxLayout()
        createLabel = QtWidgets.QLabel("Create Task List")
        createTab = self.createTable(createtasks)
        doneLabel = QtWidgets.QLabel("Done Task List")
        doneTab = self.createTable(donetasks)
        layout.addWidget(createLabel)
        layout.addWidget(createTab)
        layout.addWidget(doneLabel)
        layout.addWidget(doneTab)
        
        taskDialog.setLayout(layout)
        taskDialog.show()
                

    def createTable(self, tasks):
       # Create table
        tableWidget = QtWidgets.QTableWidget()
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.setRowCount(len(tasks) if len(tasks) > 0 else 1)
        tableWidget.setColumnCount(1)
        tableWidget.setColumnWidth(0, 380)
        if len(tasks) > 0:
            for i, j in enumerate(tasks):
                tableWidget.setCellWidget(i, 0, QtWidgets.QLabel(" " + j.format_text()))
        else:
            tableWidget.verticalHeader().setVisible(False)
            tableWidget.setCellWidget(0, 0, QtWidgets.QLabel("No tasks"))
        return tableWidget
        
