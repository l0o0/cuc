from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui 
from task import TaskLine


class TaskCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super(TaskCalendar, self).__init__(parent)
    
    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        if date.day() % 5 == 0: # example condition based on date
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtCore.Qt.red)
            painter.drawEllipse(rect.topLeft() + QtCore.QPoint(12, 7), 5, 5)
            painter.setBrush(QtCore.Qt.green)
            painter.drawEllipse(rect.topRight() + QtCore.QPoint(-12, 7), 5, 5)


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
        # task summary bar at buttom
        self.label = QtWidgets.QLabel("Click to see!")
        self.label.setFixedHeight(15)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
    
    def showDate(self, date):
        self.label.setText(date.toString())