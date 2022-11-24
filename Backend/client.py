import socket
import threading
import os
import platform

# Create one client socket


def connection_to_server():
    global client
    # Ask for server IP and port
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    client.send(platform.system().encode())         
    print(f"Client connected to server")
    data = client.recv(1024).decode()
    print(data)


def receive_data_linux(client):
    while True:
        data = client.recv(1024).decode()
        print(f"Server send: {data}")
        if data == "exit": # Close the connection when client send "exit" message
            client.close()
            print (f"Client closed by server")
            break
        elif data == "close":  # Close the client connection but not the server if client send "close"
            print("Server disconnected")
            client.close()
            break
        elif data == "os":
            # Get the os name
            os_name = os.name
            client.send(platform.system().encode())

def receive_data_windows(client):
    while True:
        data = client.recv(1024).decode()
        print(f"Server send: {data}")
        if data == "exit": # Close the connection when client send "exit" message
            client.close()
            print (f"Client closed by server")
            break
        elif data == "close":  # Close the client connection but not the server if client send "close"
            print("Server disconnected")
            client.close()
            break
        elif data == "os":
            # Get the os name
            os_name = os.name
            client.send(platform.system().encode())

def receive_data_mac(client):
    while True:
        data = client.recv(1024).decode()
        print(f"Server send: {data}")
        if data == "exit": # Close the connection when client send "exit" message
            client.close()
            print (f"Client closed by server")
            break
        elif data == "close":  # Close the client connection but not the server if client send "close"
            print("Server disconnected")
            client.close()
            break
        elif data == "os":
            # Get the os name
            os_name = os.name
            client.send(platform.system().encode())

def receive_data_nonsup(client):
    while True:
        data = client.recv(1024).decode()
        print(f"Server send: {data}")
        if data == "exit": # Close the connection when client send "exit" message
            client.close()
            print (f"Client closed by server")
            break
        elif data == "close":  # Close the client connection but not the server if client send "close"
            print("Server disconnected")
            client.close()
            break
        elif data == "os":
            # Get the os name
            os_name = os.name
            client.send("OS not supported".encode())     

def send_data(client):
    while True:
        message = input("Enter your message: ") # Possible to send message to the server
        client.send(message.encode())
        if message == "exit": # Close the server when client send "exit" message
            client.close()
            break
        elif message == "close": # Close the client connection but not down the server if client send "close"
            print ("Client disconnected")
            break

def main():
    connection_to_server()
    os = platform.system()
    if os == "Linux":
        print("Linux machine")
        receive_thread = threading.Thread(target=receive_data_linux, args=[client])
        receive_thread.start()
        send_thread = threading.Thread(target=send_data, args=[client])
        send_thread.start()
    elif os == "Windows":
        print("Windows machine")
        receive_thread = threading.Thread(target=receive_data_windows, args=[client])
        receive_thread.start()
        send_thread = threading.Thread(target=send_data, args=[client])
        send_thread.start()
    elif os == "Darwin":
        print("Mac machine")
        receive_thread = threading.Thread(target=receive_data_mac, args=[client])
        receive_thread.start()
        send_thread = threading.Thread(target=send_data, args=[client])
        send_thread.start()
    else:
        print("OS not supported, you can't use the full capacity of this program")
        receive_thread = threading.Thread(target=receive_data_nonsup, args=[client])
        receive_thread.start()
        send_thread = threading.Thread(target=send_data, args=[client])
        send_thread.start()
    
    
    


if __name__ == '__main__':
    main()

