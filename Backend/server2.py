import socket
import threading
import platform
import psutil


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 10038))
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
        threading.Thread(target=receive_data, args=[client]).start()

def receive_data(client):
    if os == 'Linux':
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'os':
                osfull = platform.platform()
                client.send(osfull.encode('utf-8'))
            elif data == 'close':
                client.close()
                # Client can reconnect
                accept_clients()
                print('Client disconnected')
                break
            elif data == 'ram':
                ram = round(psutil.virtual_memory().total / (1024.0 **3))
                ramused = round(psutil.virtual_memory().used / (1024.0 **3))
                ramfree = round(psutil.virtual_memory().free / (1024.0 **3))
                client.send(str(f"RAM T: {ram} GB, RAM U: {ramused} GB, RAM F: {ramfree} GB").encode('utf-8'))
            elif data == 'hostname':
                hostname = platform.node()
                client.send(f"HOSTNAME:{hostname}".encode('utf-8'))
            elif data == 'ip':
                ip = socket.gethostbyname(socket.gethostname())
                client.send(f"PUBLIC IP:{ip}".encode('utf-8'))
            elif data == 'cpu':
                cpu = psutil.cpu_percent()
                client.send(f"CPU:{cpu}".encode('utf-8'))
            # si data commence par Linux:

               
def send_data(client):
    while True:
        data = input('Enter command: ')
        client.send(data.encode('utf-8'))

def main():
    threading.Thread(target=accept_clients, args=[]).start()

if __name__ == '__main__':
    main()
