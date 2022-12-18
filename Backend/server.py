import socket
import threading
import platform
import psutil
import subprocess


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 10051))
server.listen(5)
os = platform.system()

# Automatically accept the connection of many supervisors
def accept_clients():
    global client
    while True:
        try: 
            print('Waiting for connection...')
            client, addr = server.accept()
            print(f'Admin with, {addr} connected') 
            client.send(f'Welcome to the server! You are connected to {os} machine.'.encode('utf-8'))
            threading.Thread(target=receive_data, args=[client]).start()
        except Exception as e:
            print(f'Error: {e}')
            pass

def receive_data(client):
    if os == 'Linux':
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'os':
                osfull = platform.system()
                client.send(f"OS: {osfull}".encode('utf-8'))
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
            # si data commence par Linux:
            elif data == 'cpu':
                cpu = psutil.cpu_percent()
                # Send cpu name and 
                client.send(f"CPU USAGE:{cpu}%".encode('utf-8'))
            # If data starts with Linux:
            elif data.startswith('Linux:'):
                try:
                    command = data.split(':')[1]
                    # Execute the command
                    output = subprocess.check_output(command, shell=True) 
                    # If output is superior to 1024 bytes
                    if len(output) > 1024:
                        # Split the output in 1024 bytes chunks
                        output = output.split(b'1024')
                        # Send the chunks
                        for chunk in output:
                            client.send(chunk)
                    else:
                        client.send(output)
                    # client.send('Command received successfully'.encode('utf-8'))
                    # client.send(output)
                except Exception as e:
                    client.send(f"Error returned by server: {e}".encode('utf-8'))         
   
    elif os == 'Windows':
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'os':
                osfull = platform.system()
                client.send(f"OS: {osfull}".encode('utf-8'))
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
            # si data commence par Linux:
            elif data == 'cpu':
                cpu = psutil.cpu_percent()
                # Send cpu name and 
                client.send(f"CPU USAGE:{cpu}%".encode('utf-8'))
            # If data starts with Linux:
            elif data.startswith('Windows:'):
                pass
    elif os == 'Darwin':
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if data == 'os':
                osfull = platform.system()
                client.send(f"OS: {osfull}".encode('utf-8'))
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
            # si data commence par Linux:
            elif data == 'cpu':
                cpu = psutil.cpu_percent()
                # Send cpu name and 
                client.send(f"CPU USAGE:{cpu}%".encode('utf-8'))
            # If data starts with Linux:
            elif data.startswith('MacOS:'):
                pass
                         
# def send_data(client):
#     while True:
#         data = input('Enter command: ')
#         client.send(data.encode('utf-8'))

def main():
    threading.Thread(target=accept_clients, args=[]).start()

if __name__ == '__main__':
    main()
