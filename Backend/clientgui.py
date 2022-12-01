import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import socket
import platform
import multiprocessing

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
        self.setGeometry(100, 100, 1200, 1200)

        #Items
        self.connect = QPushButton("Add new server")
        self.listservers = QListWidget()
        self.text = QLabel("Les serveurs enrégistrés :")
        
        # Readonly QPlainTextEdit for the logs
        self.serverreply = QTextBrowser()
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
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.disconnect = QPushButton("Disconnect")
        self.buttonconnect = QPushButton("Connect")
        self.delete = QPushButton("Delete")
        self.threadreceiv = None
        self.commandmode = QCheckBox(text="Command mode")

        # self.threadreceiv = threading.Thread(target=self.__receive_data, args=(self.client,))
        # self.exit_event = threading.Event()


        #Layout
        grid.addWidget(self.text, 0, 0)
        grid.addWidget(self.delete, 0, 1)
        grid.addWidget(self.disconnect, 0,2)
        grid.addWidget(self.listservers, 1, 0 , 1, 3)
        grid.addWidget(self.inputip, 2, 0)
        grid.addWidget(self.inputport, 2, 1)
        grid.addWidget(self.connect, 2, 2)
        grid.addWidget(self.serverreply, 3, 0, 1, 3)
        grid.addWidget(self.inputcommand, 4, 0, 1, 2)
        grid.addWidget(self.sendcommand, 4, 2, 1, 2)
        grid.addWidget(self.commandmode, 6, 0, 1, 2)
        grid.addWidget(self.presavebuttontypeos, 5, 0)
        grid.addWidget(self.presavebuttonram, 5, 1)
        grid.addWidget(self.presavebuttonhostname, 5, 2, 1, 2)

        #Events
        #Begin with list append with csv file
        self.__appendlist_server(client)
        self.connect.clicked.connect(self.__connect)
        self.listservers.itemDoubleClicked.connect(self.__chose_server)
        self.sendcommand.clicked.connect(self.__send_data)
        self.presavebuttontypeos.clicked.connect(self.__typeos)
        self.presavebuttonram.clicked.connect(self.__raminfo)
        self.presavebuttonhostname.clicked.connect(self.__hostname)
        self.disconnect.clicked.connect(self.__disconnect)
        self.delete.clicked.connect(self.__delete_server)
        # When enter is pressed, send the command
        self.inputcommand.returnPressed.connect(self.sendcommand.click)




        #Functions
    def __connect(self, client):
        if self.inputip.text() == "" or self.inputport.text() == "":
            QMessageBox.warning(self, "Error", "Please enter IP address and port")
        #else add to list ip:port
        else:
            self.listservers.addItem(self.inputip.text() + ":" + self.inputport.text())
            servercsv = open("servers.csv", "a")
            servercsv.write("\n" + self.inputip.text() + ":" + self.inputport.text())
            # servercsv.write(self.inputip.text() + ":" + self.inputport.text() + "\n")
            servercsv.close()
            self.inputip.setText("")
            self.inputport.setText("")
            #Add client to csv file 
            
    def __appendlist_server(self, client):
        servercsv = open("servers.csv", "r")
        for line in servercsv:
            self.listservers.addItem(line)
        servercsv.close()

    def __delete_server(self):
        if self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            self.listservers.takeItem(self.listservers.currentRow())
            servercsv = open("servers.csv", "w")
            for i in range(self.listservers.count()):
                servercsv.write(self.listservers.item(i).text() + "\n")
            servercsv.close()

        #Delete from csv file

    def __chose_server(self, client):
        if self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip = self.listservers.currentItem().text().split(":")[0]
                port = int(self.listservers.currentItem().text().split(":")[1])
                self.client.connect((ip, port))
                self.threadreceiv = ThreadReceive(self.client, self.serverreply)
                self.threadreceiv.start()
                QMessageBox.information(self, "Success", "Connected to server")
                #Start ThreadReceive here
                return self.client 
            except:
                QMessageBox.warning(self, "Error", "Connection failed")

    def __disconnect(self):
        if self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        try:
            self.client.send("close".encode('utf-8'))
            self.client.close()
            #self.exit_event.set()
            self.threadreceiv.terminate()
            QMessageBox.information(self, "Success", "Disconnected from server")
            self.serverreply.clear()
        except:
            QMessageBox.warning(self, "Error", "Disconnection failed")

    def __send_data(self, client):
        if self.commandmode.isChecked():
            self.client.send(f"Linux:{self.inputcommand.text()}".encode('utf-8'))
            self.inputcommand.setText("")
        if self.inputcommand.text() == "clear":
            self.serverreply.clear()
            self.inputcommand.setText("")
        elif self.inputcommand.text() == "":
            QMessageBox.warning(self, "Error", "Please enter a command")
        elif self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            self.client.send(self.inputcommand.text().encode('utf-8'))
            self.inputcommand.setText("")

    def __typeos(self):
        self.inputcommand.setText("os")
        self.__send_data(client)

    def __raminfo(self):
        self.inputcommand.setText("ram")
        self.__send_data(client)
        
    def __hostname(self):
        self.inputcommand.setText("hostname")
        self.__send_data(client)


class ThreadReceive(QThread):
    def __init__(self, client, serverreply):
        super().__init__()
        self.client = client
        self.serverreply = serverreply
        self.exit_event = threading.Event()

    def run(self):
        flag = True
        while flag == True:
            if self.exit_event.is_set():
                print ("exit")
                flag = False
            try:
                data = self.client.recv(1024)
                self.serverreply.append(f"Client> {data.decode('utf-8')}")
                # Refresh the QPlainTextEdit
                self.serverreply.verticalScrollBar().setValue(self.serverreply.verticalScrollBar().maximum())
                self.serverreply.update()
            except:
                pass
    

    def stop(self):
        self.exit_event.set()
        self.wait()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
   
  

if __name__ == '__main__':
    main()



