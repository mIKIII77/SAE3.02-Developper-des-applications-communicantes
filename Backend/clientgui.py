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
        self.setGeometry(100, 100, 700, 700)

        #Items
        self.connect = QPushButton("Add new server")
        self.listservers = QListWidget()
        self.text = QLabel("Les serveurs enrégistrés :")
        
        # Readonly QPlainTextEdit for the logs
        self.serverreply = QPlainTextEdit()
        self.serverreply.setReadOnly(True)
        #readonly

        self.inputip = QLineEdit()
        self.inputip.setPlaceholderText("Enter IP address")
        self.inputport = QLineEdit()
        self.inputport.setPlaceholderText("Enter port")
        self.inputcommand = QLineEdit()
        self.inputcommand.setPlaceholderText("Enter command")
        self.sendcommand = QPushButton("Send command")
        self.presavebuttontypeos = QPushButton("Type OS")
        self.presavebuttonram = QPushButton("RAM Info")
        self.presavebuttonhostname = QPushButton("Hostname")

        #Layout
        grid.addWidget(self.text, 0, 0)
        grid.addWidget(self.listservers, 1, 0 , 1, 3)
        grid.addWidget(self.inputip, 2, 0)
        grid.addWidget(self.inputport, 2, 1)
        grid.addWidget(self.connect, 2, 2)
        grid.addWidget(self.serverreply, 3, 0, 1, 3)
        grid.addWidget(self.inputcommand, 4, 0, 1, 2)
        grid.addWidget(self.sendcommand, 4, 2, 1, 2)
        grid.addWidget(self.presavebuttontypeos, 5, 0)
        grid.addWidget(self.presavebuttonram, 5, 1)
        grid.addWidget(self.presavebuttonhostname, 5, 2, 1, 2)

        #Events
        self.connect.clicked.connect(self.__connect)
        self.listservers.itemDoubleClicked.connect(self.__chose_server)
        self.sendcommand.clicked.connect(self.__send_data)
        self.presavebuttontypeos.clicked.connect(self.__typeos)
        self.presavebuttonram.clicked.connect(self.__raminfo)
        self.presavebuttonhostname.clicked.connect(self.__hostname)


        
        

        
        
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
        global client
        if self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip = self.listservers.currentItem().text().split(":")[0]
                port = int(self.listservers.currentItem().text().split(":")[1])
                client.connect((ip, port))
                QMessageBox.information(self, "Success", "Connected to server")
                threading.Thread(target=self.__receive_data, args=[client]).start()
                return activeconnection == True
            except:
                QMessageBox.warning(self, "Error", "Connection failed")
                return client


    def __receive_data(self, client):
        while True:
            data = client.recv(1024).decode('utf-8')
            #Write data to QPlainTextEdit at new line
            self.serverreply.appendPlainText(data)
            #write
            if data == "close":
                client.close()
                break
      

    def __send_data(self, client):
        if self.inputcommand.text() == "":
            QMessageBox.warning(self, "Error", "Please enter a command")
        elif activeconnection == False:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            client.send(self.inputcommand.text().encode('utf-8'))
            self.inputcommand.setText("")

    def __typeos(self):
        self.inputcommand.setText("os")
        self.__send_data()

    def __raminfo(self):   
        self.inputcommand.setText("ram")
        self.__send_data()

    def __hostname(self):
        self.inputcommand.setText("hostname")
        self.__send_data()


def main():
    global activeconnection
    activeconnection = False
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
  

if __name__ == '__main__':
    main()



