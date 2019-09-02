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

from task import Tasks, TaskLine



class TableWidgetDragRows(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)



    def dropEvent(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()
        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()


    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & QtCore.Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()



class HiddenLabel(QLabel):
    '''
    QLable hide when mouse pressed
    '''
    def __init__(self, buddy, taskline, parent = None):
        super(HiddenLabel, self).__init__(parent)
        self.setFixedHeight(25)
        self.buddy = buddy
        self.taskline = taskline

    # When it's clicked, hide itself and show its buddy
    #def mousePressEvent(self, event):
    #    # left click to edit 
    #    if event.button() == QtCore.Qt.LeftButton:
    #        self.hide()
    #        self.buddy.setText(self.taskline.plain_text)
    #        self.buddy.show()
    #        self.buddy.setFocus() # Set focus on buddy so user doesn't have to click again
#


class EditableCell(QWidget):
    '''
    QLineEdit show when HiddenLabel is hidden
    '''
    def __init__(self, taskline, parent = None):
        super(EditableCell, self).__init__(parent)
        self.taskline = taskline
        # Create ui
        self.myEdit = QLineEdit()
        self.myEdit.setFixedHeight(25)
        self.myEdit.hide() # Hide line edit
        self.myEdit.returnPressed.connect(self.textEdited)
        # Create our custom label, and assign myEdit as its buddy
        self.myLabel = HiddenLabel(self.myEdit, self.taskline) 
        self.myLabel.setText(self.taskline.enrich_text())

        # Put them under a layout together
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.myLabel)
        hLayout.addWidget(self.myEdit)
        hLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hLayout)

    def textEdited(self):
        # If the input is left empty, revert back to the label showing
        print('edit finished')
        print(self.myEdit.text())
        taskline = TaskLine()
        taskline.parser(self.myEdit.text())
        self.taskline = taskline
        self.myLabel.setText(taskline.enrich_text())
        self.myEdit.hide()
        self.myLabel.show()
        self.myLabel.setFocus()



class App(QWidget):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.title = 'Keep Going'
        self.left = 10
        self.top = 10
        self.width = 480
        self.height = 360
        self.initTask()
        self.initUI()
        self.tab1()
        self.tab2()
        self.tab3()
        self.initTab()


    def initTask(self):
        self.tasks = Tasks(config['todotxt'], config['donetxt'])
        self.tasks.readFromFile()
        for i in self.tasks.tasklines:
            print(i.plain_text)
        print('-'*20)

        
    def initUI(self):
        
        self.setWindowTitle(self.title)
        # 设置窗口固定大小
        self.setFixedSize(self.width, self.height)
        # 设置窗体无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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

        # add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        #print('tabs', self.tabs.geometry())

        # tab1 
    def tab1(self):
        self.tab1 = QWidget()
        self.tab1.layout = QGridLayout()
        self.tab1.layout.setVerticalSpacing(2)

        # add text edit line for new task
        self.textboxAdd = QLineEdit()
        self.textboxAdd.setPlaceholderText('Input something ...')
        self.textboxAdd.setFixedHeight(25)
        self.textboxAdd.setFixedWidth(436)
        self.tab1.layout.addWidget(self.textboxAdd, 0, 0, 1, 10)
        self.textboxAdd.returnPressed.connect(self.addLine)

        # add layout for added tasks
        self.tab1TaskTable = QTableWidget()
        self.tab1TaskTable.verticalHeader().setVisible(False)
        self.tab1TaskTable.horizontalHeader().setVisible(False)
        #self.tab1TaskTable.setShowGrid(False)
        self.tab1TaskTable.setColumnCount(3)
        self.tab1TaskTable.setRowCount(len(self.tasks.tasklines))
        self.tab1TaskTable.setColumnWidth(0, 380)
        self.tab1TaskTable.setColumnWidth(1, 20)
        self.tab1TaskTable.setColumnWidth(2, 20)
        self.tab1TaskTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tab1.layout.addWidget(self.tab1TaskTable, 1, 0, 15, 13)
        print(self.tab1TaskTable.geometry())

        # add widget for menu button
        self.tab1Pin = QPushButton()
        self.tab1Pin.setMaximumSize(30, 30)
        self.tab1Pin.setCheckable(True)
        self.tab1Pin.setIcon(QIcon("icons/pinterest2.png"))
        self.tab1Pin.clicked.connect(self.winPinTop)
        self.tab1Menu = QPushButton()
        self.tab1Menu.setMaximumSize(30, 30)
        self.tab1Menu.setChecked(True)
        self.tab1Menu.setIcon(QIcon("icons/cog.png"))
        self.tab1.layout.addWidget(self.tab1Pin,16, 9)
        self.tab1.layout.addWidget(self.tab1Menu,16, 10)
        # display tasks
        for i, t in enumerate(self.tasks.tasklines):
            print('init row %s' % i)
            cellwidget = self.createCellQlabel(t)
            self.tab1TaskTable.setCellWidget(i, 0, cellwidget)
            editButton = self.createButton('edit')
            deleteButton = self.createButton('delete')            
            self.tab1TaskTable.setCellWidget(i,1, editButton)
            self.tab1TaskTable.setCellWidget(i,2, deleteButton)
        print('init table rows ', self.tab1TaskTable.rowCount())
        self.tab1.setLayout(self.tab1.layout)

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


        
    def closeEvent(self, event):
        event.ignore()
        self.hide()


    def rightBottomShow(self):
        self.setGeometry(*self.fixedGeometry)
        self.show()
    

    def createButton(self, t):
        self.butt = QPushButton()
        self.butt.setMaximumSize(25, 25)
        if t == 'delete':
            self.butt.setIcon(QIcon("icons/cancel-circle.png"))      
            self.butt.clicked.connect(self.deleteButtonAction)     
        elif t == 'edit':
            self.butt.setIcon(QIcon("icons/pen.png"))
            self.butt.clicked.connect(self.editButtonAction)
        return self.butt


    def createCellQlabel(self, taskline):
        cellwidget = EditableCell(taskline) 
        return cellwidget       


    def addLine(self):
        #QMessageBox.information(self, "Info", "Enter Pressed.")
        print('total rows before', self.tab1TaskTable.rowCount())
        if not self.textboxAdd.text().strip():
            QMessageBox.information(self, "Info", "Input something")
        else:
            rowidx = 0
            self.tab1TaskTable.insertRow(rowidx)
            taskline = TaskLine()
            taskline.parser(self.textboxAdd.text())
            cellwidget = self.createCellQlabel(taskline)
            self.tab1TaskTable.setCellWidget(rowidx, 0, cellwidget)
            editButton = self.createButton('edit')
            deleteButton = self.createButton('delete')
            self.tab1TaskTable.setCellWidget(rowidx, 1, editButton)
            self.tab1TaskTable.setCellWidget(rowidx, 2, deleteButton)
            self.textboxAdd.clear()
            self.tasks.tasklines.insert(0, taskline)
        print('total rows after', self.tab1TaskTable.rowCount())


    @QtCore.pyqtSlot()
    def editButtonAction(self):
        button = self.sender()
        if button:
            row = self.tab1TaskTable.indexAt(button.pos()).row()
            self.editcellwidget = self.tab1TaskTable.cellWidget(row, 0)
            self.editcellwidget.myLabel.hide()
            self.editcellwidget.myEdit.setText(self.editcellwidget.taskline.plain_text)
            self.editcellwidget.myEdit.show()
            self.editcellwidget.myEdit.setFocus()
            self.editcellwidget.myEdit.returnPressed.connect(self.editButtonAction2) 
            self.tasks.tasklines[row] = self.editcellwidget.taskline
            self.tab1TaskTable.setCellWidget(row, 0, self.editcellwidget)
            print('edit ', row, self.tasks.tasklines[row].plain_text)


    def editButtonAction2(self):
        # If the input is left empty, revert back to the label showing
        print('edit finished2')
        print(self.editcellwidget.myEdit.text())
        taskline = TaskLine()
        taskline.parser(self.editcellwidget.myEdit.text())
        self.editcellwidget.taskline = taskline
        self.editcellwidget.myLabel.setText(taskline.enrich_text())
        self.editcellwidget.myEdit.hide()
        self.editcellwidget.myLabel.show()
        self.editcellwidget.myLabel.setFocus()

    
    @QtCore.pyqtSlot()
    def deleteButtonAction(self):
        button = self.sender()
        if button:
            row = self.tab1TaskTable.indexAt(button.pos()).row()
            #column = self.tab1TaskTable.column(button)
            self.tab1TaskTable.removeRow(row)
            del self.tasks.tasklines[row]
        print('delete', row)


    @QtCore.pyqtSlot()
    def winPinTop(self):
        button = self.sender()
        if button.isChecked():
            print('on top')
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
            self.rightBottomShow()
        else:
            print('no top')
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
        self.parent.tasks.saveToFile()
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
    app = QApplication(sys.argv)
    ex = App(config)
    trayIcon = SystemTrayIcon(QIcon("icons/icon.png"), ex)
    trayIcon.show()
    sys.exit(app.exec_())
