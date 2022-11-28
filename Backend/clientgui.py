import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import socket
import platform

#Import backend files with path: Backend/
import client as client

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("SuperVision")
        self.setGeometry(100, 100, 1600, 1000)
        
        #Items
        self.connect = QPushButton("Add new server")
        self.listservers = QListWidget()
        text = QLabel("Les serveurs enrégistrés :")
        serverreply = QTextEdit()
        self.inputip = QLineEdit()
        self.inputip.setPlaceholderText("Enter IP address")
        self.inputport = QLineEdit()
        self.inputport.setPlaceholderText("Enter port")
        inputcommand = QLineEdit()
        inputcommand.setPlaceholderText("Enter command")
        sendcommand = QPushButton("Send command")
        presavebuttontypeos = QPushButton("Type OS")
        presavebuttonram = QPushButton("RAM Info")
        presavebuttonhostname = QPushButton("Hostname")

        #Layout
        grid.addWidget(text, 0, 0)
        grid.addWidget(self.listservers, 1, 0 , 1, 3)
        grid.addWidget(self.inputip, 2, 0)
        grid.addWidget(self.inputport, 2, 1)
        grid.addWidget(self.connect, 2, 2)
        grid.addWidget(serverreply, 3, 0, 1, 3)
        grid.addWidget(inputcommand, 4, 0, 1, 2)
        grid.addWidget(sendcommand, 4, 2, 1, 2)
        grid.addWidget(presavebuttontypeos, 5, 0)
        grid.addWidget(presavebuttonram, 5, 1)
        grid.addWidget(presavebuttonhostname, 5, 2, 1, 2)

        #Events
        self.connect.clicked.connect(self.__connect)
        self.listservers.itemDoubleClicked.connect(self.__chose_server)

        #Functions
    def __connect(self):
        if self.inputip.text() == "" or self.inputport.text() == "":
            QMessageBox.warning(self, "Error", "Please enter IP address and port")
        #else add to list ip:port
        else:
            self.listservers.addItem(self.inputip.text() + ":" + self.inputport.text())
            self.inputip.setText("")
            self.inputport.setText("")
    
    def __chose_server(self):
        if self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip = self.listservers.currentItem().text().split(":")[0]
                port = int(self.listservers.currentItem().text().split(":")[1])
                client.connect((ip, port))
                QMessageBox.information(self, "Success", "Connected to server")
            except:
                QMessageBox.warning(self, "Error", "Connection failed")
                return
    def __print_server_reply(self):
        reply = client.receive_data(client)
        # Write reply in serverreply QTextEdit
        
            


            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    

