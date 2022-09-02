import sys, os
import qdarkstyle
import qtawesome as qta
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading

#Loading widgets and workflow
from workflowMain import *
from guiWidgets import *

class emittingStream(QObject): 
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

## This is the meain gui
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'ConCISE'
        sys.stdout = emittingStream(textWritten=self.normalOutputWritten)

        #self.TEST = True # This is only for Testing the code

        if sys.platform == "linux" or sys.platform == "linux2":
            self.system = "linux"
        elif sys.platform == "darwin":
            self.system = "darwin"
        elif sys.platform == "win32" or sys.platform == "win64":
            self.system = "windows"


        if self.system == 'linux':
            self.key = "Ctrl"
        elif self.system == 'darwin':
            self.key = "Cmnd"
        elif self.system == 'windows':
            self.key = "Ctrl"

        # self.createMenuBar()
        self.initUI()

        self.runner = wfRunner()
        
    # Starting the thread which will capture all exports from the workflow
    def start_task(self, task, canopus, network, export):
        var = self.output.toPlainText()
        self.thread = threading.Thread(target=self.runner.runWorkFlow, args=(task, canopus, network, export))
        self.thread.start()

    def __del__(self):  # test
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    # Printing everything written to the terminal into the text edit box
    def normalOutputWritten(self, text):  # test
        """Append text to the QTextEdit."""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()

    def initUI(self):
        def resource_path(relative_path):
         if hasattr(sys, '_MEIPASS'):
             return os.path.join(sys._MEIPASS, relative_path)
         return os.path.join(os.path.abspath("."), relative_path)

        # Setting Window Geometry
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 700, 700)
        self.statusBar().showMessage('Ready')

        #Defining scroll area
        scroll = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        # Adding Widgets
        self.toplabel = QLabel(self)
        self.toplabel.setFont(QFont('Arial', 22))
        self.toplabel.setText("ConCISE: Consensus Classifications of In Silico Elucidations")
        self.toplabel.setContentsMargins(0,0,0,15)
        layout.addWidget(self.toplabel)

        
        # Task ID Title:
        labelWidget = iconLabel()
        labelWidget.label.setText("GNPS Task ID")
        labelWidget.help.setToolTip('GNPS Task ID which can be found in the url for your job following "task="')
        layout.addWidget(labelWidget)

        #Task ID line Edit
        self.taskId = QLineEdit(self)
        self.taskId.setPlaceholderText("Enter your GNPS task ID")
        self.taskId.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.taskId.setContentsMargins(0,0,0,10)
        layout.addWidget(self.taskId)

        #Adding file selectors
        #Label for canopus
        self.canopusLabel = iconLabel()
        self.canopusLabel.label.setText("CANOPUS summary file")
        self.canopusLabel.help.setToolTip("Called canopus_summary.tsv in SIRIUS 4 or canopus_compound_summary.tsv in SIRIUS 5")

        #Canopus file line edit
        self.canopus = fileSearch()
        self.canopus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.canopus.setContentsMargins(0,0,0,10)

        #Network info label
        self.networkLabel = iconLabel()
        self.networkLabel.label.setText("Network info file")
        self.networkLabel.help.setToolTip("Network info tsv exported from the clusterinfo_summary subdirectory downloaded from GNPS")

        #Network file line edit
        self.network = fileSearch()
        self.network.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.network.setContentsMargins(0,0,0,10)

        #Export label
        self.exportLabel = iconLabel()
        self.exportLabel.label.setText("Export directory")
        self.exportLabel.help.setToolTip("Where do you want to save the ConCISE summary file?")

        #Export line edit
        self.export = dirSearch()
        self.export.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.export.setContentsMargins(0,0,0,10)
        
        #Adding all the widgets
        layout.addWidget(self.canopusLabel)
        layout.addWidget(self.canopus)
        layout.addWidget(self.networkLabel)
        layout.addWidget(self.network)
        layout.addWidget(self.exportLabel)
        layout.addWidget(self.export)

        # Make website button
        self.mkConsensus = QPushButton("Build Consensus", self)
        self.mkConsensus.clicked.connect(self.makeClick)
        self.mkConsensus.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.mkConsensus)

        # Making text edit
        self.output = QTextEdit(self)
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.output)

        #Setting scroll area as central widget
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)



    

    @pyqtSlot()
    def quit(self):
        sys.exit()

    def makeClick(self):
        task = self.taskId.text()
        canopusFile = self.canopus.searchDirectory.text()
        networkFile = self.network.searchDirectory.text()
        exportDir = self.export.searchDirectory.text()

        mkErr = "None!"

        #This test section is only for testing the gui without inputting everything manually
        #if self.TEST:
                #task = '16616afa8edd490ea7e50cc316a20222'
                #canopusFile = '/Users/zacharyquinlan/Documents/GitHub/conCISE/src/notebookTestFiles/canopus_summary.tsv'
                #networkFile = '/Users/zacharyquinlan/Documents/GitHub/conCISE/src/notebookTestFiles/Node_info.tsv'
                #exportDir = '/Users/zacharyquinlan/Documents/temp.nosync'

        ##Errors out if no files are selected
        #Task ID Erorr
        if task == None:
            mkErr = 'no task ID'
            message = QMessageBox.question(self, "Error", "No GNPS task ID provided", QMessageBox.Cancel, QMessageBox.Cancel)

        #Canopus file error
        if not os.path.isfile(canopusFile):

            mkErr = "no canopus selected"
            message = QMessageBox.question(self, "Error", "No canopus file selected", QMessageBox.Cancel, QMessageBox.Cancel)

        #network file error
        if not os.path.isfile(networkFile):

            mkErr = "no network selected"
            message = QMessageBox.question(self, "Error", "No network file selected", QMessageBox.Cancel, QMessageBox.Cancel)


        if mkErr == 'None!':
            startThread = self.start_task(task, canopusFile, networkFile, exportDir)

        self.statusBar().clearMessage()
        self.statusBar().showMessage('Ready')






if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = mainWindow()
    win.show()

    sys.exit(app.exec_())



