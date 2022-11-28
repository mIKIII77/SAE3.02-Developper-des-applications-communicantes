import socket
import threading
import os
import platform

os_name = platform.system()

# Connect to many servers
def connect_to_servers():
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1:10018"))
        server.listen(5)
        print('Waiting for connection...')
        client, addr = server.accept()
        print(f'Admin with, {addr} connected') 



def send_data(client):
    while True:
        data = input('Enter data: ')
        client.send(data.encode('utf-8'))
        if data == 'close':
            client.close()
            break

def receive_data(client):
    while True:
        data = client.recv(1024).decode('utf-8')
        print(data)

def main():
    connect_to_server()
    print('Connected to server')
    thread_send = threading.Thread(target=send_data, args=[client])
    thread_send.start()
    thread_receive = threading.Thread(target=receive_data, args=[client])
    thread_receive.start()

if __name__ == '__main__':
    main()