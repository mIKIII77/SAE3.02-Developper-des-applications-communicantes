import socket
import threading
import platform


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 10019))
server.listen(5)
os = platform.system()

# Automatically accept the connection of many supervisors
def accept_clients():
    global client
    while True:
        print('Waiting for connection...')
        client, addr = server.accept()
        print(f'Admin with, {addr} connected') 
        client.send(f'Welcome to the server! You are connected to {os}.'.encode('utf-8'))


def receive_data(client):
    if os == 'Linux':
        while True:
            data = client.recv(1024).decode('utf-8')
            if data == 'os':
                client.send(os.encode('utf-8'))
            elif data == 'close':
                client.close()
                break

def send_data(client):
    while True:
        data = input('Enter command: ')
        client.send(data.encode('utf-8'))

def main():
    threading.Thread(target=accept_clients, args=[]).start()

if __name__ == '__main__':
    main()
