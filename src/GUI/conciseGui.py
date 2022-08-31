import sys, os, subprocess
import qdarkstyle
import qtawesome as qta
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from queue import Queue
from workflowConciseGui import *

#File search widget
class fileSearch(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.searchDirectory = QLineEdit(self)
        self.searchDirectory.setFixedWidth(300)
        self.searchDirectory.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        icon = qta.icon('fa.file-o')
        self.findButton = QPushButton(icon, "Select File", self)
        self.findButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.findButton.clicked.connect(self.dirClick)

        layout.addWidget(self.searchDirectory, 0)
        layout.addWidget(self.findButton, 2)
        layout.setAlignment(Qt.AlignLeft)

    @pyqtSlot()
    def dirClick(self):
        # currentDirectory = self.searchDirectory.text()
        fname = QFileDialog.getOpenFileName(self, 'Select a File', '','All files (*.*)')[0] # Needs to select a file and not a folder

        if fname:
            # Returns pathName with the '/' separators converted to separators that are appropriate for the underlying operating system.
            # On Windows, toNativeSeparators("c:/winnt/system32") returns
            # "c:\winnt\system32".
            fname = QDir.toNativeSeparators(fname)

        if os.path.isfile(fname):
            self.searchDirectory.setText(fname)

#Directory search widget
class dirSearch(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.searchDirectory = QLineEdit(self)
        self.searchDirectory.setFixedWidth(300)
        self.searchDirectory.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        icon = qta.icon('fa.folder-open-o')
        self.findButton = QPushButton(icon, "Select Directory", self)
        self.findButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.findButton.clicked.connect(self.dirClick)

        layout.addWidget(self.searchDirectory, 0)
        layout.addWidget(self.findButton, 2)
        layout.setAlignment(Qt.AlignLeft)

    @pyqtSlot()
    def dirClick(self):
        currentDirectory = self.searchDirectory.text()
        fname = QFileDialog.getExistingDirectory(self, 'Select a Directory', currentDirectory)

        if fname:
            # Returns pathName with the '/' separators converted to separators that are appropriate for the underlying operating system.
            # On Windows, toNativeSeparators("c:/winnt/system32") returns
            # "c:\winnt\system32".
            fname = QDir.toNativeSeparators(fname)

        if os.path.isdir(fname):
            self.searchDirectory.setText(fname)

# Icon label for each search menu with help tooltip option
class iconLabel(QWidget):
    def __init__(self):
        super().__init__()
        questionIcon = qta.icon('fa.question-circle-o', color = 'white').pixmap(QSize(16,16))

        labelLayout = QHBoxLayout(self)
        labelLayout.setAlignment(Qt.AlignLeft)
        labelLayout.setContentsMargins(0,0,0,0)

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 15))
        self.label.setAlignment(Qt.AlignLeft)

        self.help = QLabel()
        self.help.setPixmap(questionIcon)
        self.help.setAlignment(Qt.AlignLeft)

        self.setStyleSheet("QToolTip{font: 15pt}")
        

        labelLayout.addWidget(self.label)
        labelLayout.addWidget(self.help)



## This is the meain gui
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'ConCISE'

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


    def initUI(self):
        def resource_path(relative_path):
         if hasattr(sys, '_MEIPASS'):
             return os.path.join(sys._MEIPASS, relative_path)
         return os.path.join(os.path.abspath("."), relative_path)

        # Setting Window Geometry
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 650, 500)
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
            workflowRun(task, canopusFile, networkFile, exportDir)

            # output = sys.stdout 
            # message = QMessageBox.question(self, "Success!", "Consensuses found!!", QMessageBox.Ok, QMessageBox.Ok)
            

        self.statusBar().clearMessage()
        self.statusBar().showMessage('Ready')






if __name__ == '__main__':
    # queue = Queue()
    # sys.stdout = WriteStream(queue)

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = mainWindow()
    win.show()

    sys.exit(app.exec_())



