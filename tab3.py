from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui 
from task import TaskLine


class TaskCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super(TaskCalendar, self).__init__(parent)
    
    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        if date.day() % 5 == 0: # example condition based on date
            painter.drawText(rect.bottomLeft(), "test")


class TAB3(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TAB3, self).__init__(parent)
        self.config = self.parent().config
        self.initCal()
        
    def initCal(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.cal = TaskCalendar()
        self.cal.setGridVisible(True)
        self.cal.clicked[QtCore.QDate].connect(self.showDate)
        self.layout.addWidget(self.cal)
        self.setLayout(self.layout)
    
    def showDate(self, date):
        print(date.toString())