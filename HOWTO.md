# How to use the SuperVision project ? 

In this file, I will explain how to use the SuperVision project.
Before using the SuperVision project, you need to read the [README.md](README.md) file.

Here the screenshot of the main window of the project:
<img src="HOWTO-Assets/AppScreenshot.png" alt="AppScreenshot" style="zoom:50%;" />

## List of the servers 

At the top of the window, you can see the list of the servers that are available to you to connect to them. This list append automatically when you start the project, this work with the .csv file in the SuperVisionApp/ServersList folder.

You can add a server to this list by clicking on the "Add new server" button. Befor adding a server, you need to write the IP address of the server in the "IP address" field and the port of the server in the "Port" field. Then, you can click on the "Add new server" button to add the server to the list. Once the server is added to the list, his also added to the .csv file.

You can remove a server from the list by clicking on the "Delete" button at the top of the window. Before removing a server, you need to select the server in the list. To select a server, you need to click on the server in the list. Then, you can click on the "Delete" button to remove the server from the list. Once the server is removed from the list, his also removed from the .csv file.

## Connect to a server

To connect to a server, you need to select the server in the list. After selecting the server you just need to double click on the server in the list. Once you double click on the server, the project will try to connect to the server. 

<b>If the connection is successful, the project will display an success message.</b>
<img src="HOWTO-Assets/SuccessMessage.png" alt="ConnectionSuccess" style="zoom:50%;" />

<b>If the connection is not successful, the project will display an error message like this:</b>

<img src="HOWTO-Assets/ErrorMessage.png" alt="ConnectionError" style="zoom:50%;" />

## Disconnect from a server

To disconnect from a server, you need to select the server in the list. After selecting the server you just need to click on the "Disconnect" button at the top of the window. Once you click on the "Disconnect" button, the project will try to disconnect from the server.

<b>If the disconnection is successful, the project will display an success message.</b>
<img src="HOWTO-Assets/SuccessMessageDisconnect.png" alt="DisconnectionSuccess" style="zoom:50%;"/>

<b>If the disconnection is not successful, the project will display an error message like this:</b>
<img src="HOWTO-Assets/ErrorMessageDisconnect.png" alt="DisconnectionError" style="zoom:50%;" />

Once you disconnect from a server, you can connect to another server. Also you can reconnect to the same server. Remember that you can't connect to a server if you are already connected to another server. So if try to connect to a server while you are connected to another server, the project will disconnect you automatically from the first server and will try to connect to the second server.