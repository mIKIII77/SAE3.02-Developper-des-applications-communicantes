import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import socket
import os
import datetime

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        # Window title
        self.setWindowTitle("SuperVision")
        # Window icon
        self.setWindowIcon(QIcon("Assets/vision.png"))
        # Window flags (minimize and close button, remove maximize button)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        # appid for the tray icon
        appid = 'SuperVision'  # arbitrary string

        # Colors for the app
        
        self.setGeometry(100, 100, 700, 700)
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
        self.disconnect = QPushButton("Disconnect")
        self.buttonconnect = QPushButton("Connect")
        self.delete = QPushButton("Delete")
        self.threadreceiv = None
        self.commandmode = QCheckBox(text="Command mode")
        # Dropdown List of os for command mode
        self.commandmodeos = QComboBox()
        self.logs = QPushButton("Logs")

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
        grid.addWidget(self.commandmode, 6, 0)
        grid.addWidget(self.commandmodeos, 6, 1)
        grid.addWidget(self.presavebuttontypeos, 5, 0)
        grid.addWidget(self.presavebuttonram, 5, 1)
        grid.addWidget(self.presavebuttonhostname, 5, 2, 1, 2)
        grid.addWidget(self.logs, 6, 2, 1, 2)

        #Events
        #Begin with list append with csv file
        self.__appendlist_server(client)
        # Add items to the dropdown list
        self.commandmodeos.addItem("Linux")
        self.commandmodeos.addItem("Windows")
        self.commandmodeos.addItem("MacOS")

    
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
        self.commandmode.stateChanged.connect(self.__commandmode)
        #When close window
        self.closeEvent = self.__closeEvent
        # Show logs 
        self.logs.clicked.connect(self.__show_logs)


        #Functions
    def __connect(self, client):
        if self.inputip.text() == "" or self.inputport.text() == "":
            QMessageBox.warning(self, "Error", "Please enter IP address and port")
        #else add to list ip:port
        else:
            self.listservers.addItem(self.inputip.text() + ":" + self.inputport.text())
            servercsv = open("ServersList/servers.csv", "a")
            servercsv.write("\n" + self.inputip.text() + ":" + self.inputport.text())
            # servercsv.write(self.inputip.text() + ":" + self.inputport.text() + "\n")
            servercsv.close()
            self.inputip.setText("")
            self.inputport.setText("")
            #Add client to csv file 
 
    def __show_logs(self):
        #Show directory with logs
        os.startfile("Logs")

    def __appendlist_server(self, client):
        servercsv = open("ServersList/servers.csv", "r")
        for line in servercsv:
            self.listservers.addItem(line)
        servercsv.close()

    def __delete_server(self):
        if self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        else:
            self.listservers.takeItem(self.listservers.currentRow())
            servercsv = open("ServersList/servers.csv", "w")
            for i in range(self.listservers.count()):
                servercsv.write(self.listservers.item(i).text() + "\n")
            servercsv.close()
        #Delete from csv file

    def __chose_server(self, client):
        try:
            # If the client is already connected, disconnect it
            self.client.send("close".encode('utf-8'))
            self.client.close()
            self.threadreceiv.terminate()
        except:
            pass 

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

        if self.commandmode.isChecked() and self.commandmodeos.currentText() == "Linux":
            try:
                self.client.send(f"Linux:{self.inputcommand.text()}".encode('utf-8'))
                self.inputcommand.setText("")
            except:
                QMessageBox.warning(self, "Error", "Please connect to a server")

        elif self.commandmode.isChecked() and self.commandmodeos.currentText() == "Windows":
            try:
                self.client.send(f"Windows:{self.inputcommand.text()}".encode('utf-8'))
                self.inputcommand.setText("")
            except:
                QMessageBox.warning(self, "Error", "Please connect to a server")
        
        elif self.commandmode.isChecked() and self.commandmodeos.currentText() == "MacOS":
            try:
                self.client.send(f"MacOS:{self.inputcommand.text()}".encode('utf-8'))
                self.inputcommand.setText("")
            except:
                QMessageBox.warning(self, "Error", "Please connect to a server")

        elif self.inputcommand.text() == "help":
            self.inputcommand.setText("")
            self.serverreply.append("Here is the list of commands available:")
            self.serverreply.append("● help: Show all commands")
            self.serverreply.append("● clear: Clear the server reply")
            self.serverreply.append("● close: Disconnect from server")
            self.serverreply.append("● kill: Kill the server")
            self.serverreply.append("● ram: Show the Total RAM and the RAM usage")
            self.serverreply.append("● cpu: Show the CPU usage")
            self.serverreply.append("● ip: Show the IP address of the server")
            self.serverreply.append("● os: Show the OS of the server")
            self.serverreply.append("● hostname: Show the hostname of the server")
            self.serverreply.append("● Linux:'command': Execute a Linux command")
            self.serverreply.append("● Windows:'command': Execute a Windows command")
            self.serverreply.append("● MacOS:'command': Execute a MacOS command")
            self.serverreply.append(" ")
        
        elif self.inputcommand.text() == "clear":
            self.serverreply.clear()
            self.inputcommand.setText("")
        elif self.inputcommand.text() == "":
            QMessageBox.warning(self, "Error", "Please enter a command")
        elif self.listservers.currentItem() == None:
            QMessageBox.warning(self, "Error", "Please select a server")
        
        elif self.inputcommand.text() == "close":
            try:
                self.client.send("close".encode('utf-8'))
                self.client.close()
                self.threadreceiv.terminate()
                QMessageBox.information(self, "Success", "Disconnected from server")
                self.serverreply.clear()
            except:
                QMessageBox.warning(self, "Error", "Disconnection failed or server is not connected")

        elif self.inputcommand.text() == "kill":
            try:
                self.client.send("kill".encode('utf-8'))
                self.client.close()
                self.threadreceiv.terminate()
                QMessageBox.information(self, "Success", "Disconnected from server, server was killed")
                self.serverreply.clear()
            except:
                QMessageBox.warning(self, "Error", "Disconnection failed or server is not connected")
        else:
            try:
                self.client.send(self.inputcommand.text().encode('utf-8'))
                self.inputcommand.setText("")
            except:
                QMessageBox.warning(self, "Error", "Please connect to a server")

    def __typeos(self):
        try:
            self.inputcommand.setText("os")
            self.__send_data(client)
        except:
            QMessageBox.warning(self, "Error", "Server is not connected")

    def __raminfo(self):
        try:
            self.inputcommand.setText("ram")
            self.__send_data(client)
        except:
            QMessageBox.warning(self, "Error", "Server is not connected")
        
    def __hostname(self):
        try:
            self.inputcommand.setText("hostname")
            self.__send_data(client)
        except:
            QMessageBox.warning(self, "Error", "Server is not connected")

    def __commandmode(self):
        if self.commandmode.isChecked():
            self.presavebuttonhostname.setEnabled(False)
            self.presavebuttontypeos.setEnabled(False)
            self.presavebuttonram.setEnabled(False)
        else:
            self.presavebuttonhostname.setEnabled(True)
            self.presavebuttontypeos.setEnabled(True)
            self.presavebuttonram.setEnabled(True)

    def __closeEvent(self, event):
        try:
            self.client.send("close".encode('utf-8'))
            self.client.close()
            self.threadreceiv.terminate()
        except:
            pass

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
                hostname = socket.gethostname()
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                self.serverreply.verticalScrollBar().setValue(self.serverreply.verticalScrollBar().maximum())
                self.serverreply.update()
                # Create a log file for each client
                # Write the data received from the client to the log file
                if os.path.exists(f"Logs/{hostname}-{self.client.getpeername()[0]}.log") == False:
                    log = open(f"Logs/{hostname}-{self.client.getpeername()[0]}.log", "x")
                    log.write(f"Begin log for {hostname}-{self.client.getpeername()[0]}.log")
                    log.write(f"\n--------------------------------------")
                    log.write(f"\n{current_time}---Client> {data.decode('utf-8')}")
                    log.close()
                else:
                    log = open(f"Logs/{hostname}-{self.client.getpeername()[0]}.log", "a")
                    log.write(f"\n{current_time}---Client> {data.decode('utf-8')}")
                    log.close()
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



