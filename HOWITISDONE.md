# How the SuperVision project done ?

## Connection / Disconnection / Reconnection to the server

### Connection

To connect to the server i write a function that try to connect to the server. If the connection is successful, the function wille start a thread that will listen to the server response. If the connection is not successful, the function will return an error message. This function will disconnect the client if it is already connected to a other server and stop the thread before connecting to the new server. The information of the server ip and port are taken from the list of servers. We use the variable "self.client" to store the client socket and start with it the thread. The variable "self.threadreceiv" is used to store the thread.

```python
 def __chose_server(self, client):
        try:
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
```

### Disconnection

To disconnect from the server, we use the function "__disconnect" of the socket. We also stop the thread that listen to the server response. This function will return an error message if the client don't choose a server in the list of servers to disconnect from. If the client choose a server in the list of servers, the function will try to disconnect from the server by sending the message "close" to the server.(This message is used to close the connection between the client on the server). After we close the socket variable "self.client" and stop the thread variable "self.threadreceiv". If the disconnection is successful, the function will return a success message. If the disconnection is not successful, the function will return an error message.

```python
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
```

### Reconnection

The reconnection works the same way as the connection. This action will use the same function "__chose_server". That's why at the beginning of the function "__chose_server" we disconnect the client if it is already connected to a other server and stop the thread before connecting to the new server.



## Send a message/command to the server / Receive a return from the server

### Send a message/command to the server

```python
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
                QMessageBox.warning(self, "Error", "Please connect to a server")
        
        elif self.inputcommand.text() == "kill":
            try:
                self.client.send("kill".encode('utf-8'))
                self.client.close()



We also use the function "setText" of the QLineEdit to clear the input command line.

```python
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
```
