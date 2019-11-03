from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui 
from task import TaskLine


class TAB2(QtWidgets.QWidget):
    restore_trigger = QtCore.pyqtSignal(TaskLine)
    def __init__(self, parent=None):
        super(TAB2, self).__init__(parent)
        self.config = self.parent().config
        self.doneTasks = []
        self.layout = QtWidgets.QVBoxLayout()

        # add layout for added tasks
        self.tab2TaskTable = QtWidgets.QTableWidget()
        self.tab2TaskTable.setStyleSheet("selection-background-color: #f4f6f6")
        self.tab2TaskTable.verticalHeader().setVisible(False)
        self.tab2TaskTable.horizontalHeader().setVisible(False)
        self.tab2TaskTable.setShowGrid(False)
        self.tab2TaskTable.setColumnCount(2)
        self.tab2TaskTable.setRowCount(0)
        self.tab2TaskTable.setColumnWidth(0, 415)
        self.tab2TaskTable.setColumnWidth(1, 20)
        self.tab2TaskTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.layout.addWidget(self.tab2TaskTable)

        # signal and slot
        # update tray icon by taskline number 
        self.restore_trigger.connect(self.parent().updateTab1Table)

        # display tasks
        self.layout.setContentsMargins(3,3,3,0)
        self.setLayout(self.layout)


    # create button in taskline
    def createButton(self):
        butt = QtWidgets.QPushButton()
        butt.setMaximumSize(25, 25)
        butt.setIcon(QtGui.QIcon("icons/restore.png"))      
        butt.setStyleSheet("QPushButton{border:1px;}")
        butt.clicked.connect(self.restoreButtonAction)     
        return butt

    
    def restoreButtonAction(self):
        button = self.sender()
        if button:
            row = self.tab2TaskTable.indexAt(button.pos()).row()
            self.tab2TaskTable.removeRow(row)
            taskline = self.doneTasks[row]
            taskline.mask = None
            taskline.completion_date = None
            self.restore_trigger.emit(taskline)
            del self.doneTasks[row]
        print('restore', row, taskline.format_text())
        # send signal to update tray icon

    
    def createTaskRow(self, donetask, row, tablewidget, config=None):
        if config == None:
            config = self.config.config
        cellwidget = QtWidgets.QLabel("<s>%s</s>" % donetask.enrich_text(self.config.config['style']))
        style_temp = "QLabel{padding-top:0;padding-left:5px;font-family:Arial,NotoColorEmoji;font-size:%spx}"
        cellwidget.setStyleSheet(style_temp % config['style']['fontsize'])
        tablewidget.setCellWidget(row, 0, cellwidget)
        restoreButt = self.createButton()
        tablewidget.setCellWidget(row, 1, restoreButt)    


    def saveDoneTask(self, done):
        done_texts = [t.format_text() + '\n' for t in self.doneTasks.tasklines if getattr(t, 'status', None)  != 'saved']
        with open(done, 'a', encoding='utf-8') as handle:
            handle.writelines(done_texts)
            print('save done.txt, %s' % len(self.doneTasks.tasklines))