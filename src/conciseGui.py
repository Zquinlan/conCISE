import sys, os
import qdarkstyle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#import workflow

#File search widget
class fileSearch(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.searchDirectory = QLineEdit(self)
        self.searchDirectory.setFixedWidth(300)
        self.searchDirectory.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.findButton = QPushButton("Select File", self)
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
        self.setGeometry(0, 0, 500, 400)
        self.statusBar().showMessage('Ready')

        #Defining scroll area
        scroll = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        # Adding Widgets
        # Task ID Title:
        self.taskId = QLineEdit(self)
        self.taskId.setPlaceholderText("Enter your GNPS task ID")
        self.taskId.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.taskId)

        #Adding file selectors
        #Label for canopus
        self.canopusLabel = QLabel(self)
        self.canopusLabel.setText("CANOPUS summary file")
        self.canopusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Album link line edit
        self.canopus = fileSearch()
        self.canopus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Node info label
        self.networkLabel = QLabel(self)
        self.networkLabel.setText("Network info tsv")
        self.networkLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Album link line edit
        self.network = fileSearch()
        self.network.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        #Adding all the widgets
        layout.addWidget(self.canopusLabel)
        layout.addWidget(self.canopus)
        layout.addWidget(self.networkLabel)
        layout.addWidget(self.network)

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


        self.statusBar().clearMessage()
        self.statusBar().showMessage('Fetching data from GNPS')
       


        configArgs = {'taskId' : task, 'canopusFile' : canopusFile, 'network' : networkFile}
        mkErr = "None!"


        if mkErr == 'None!':
            message = QMessageBox.question(self, "Success!", "Consensuses found!!", QMessageBox.Ok, QMessageBox.Ok)
            print(configArgs)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())