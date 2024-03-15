# echo-client.py

import socket

HOST = "ip_addr"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    name = input("Name: ")
    s.connect((HOST, PORT))
    while True:
        message = input(f"{name}: ")
        if message:
            message = f"{name}: {message}"
            s.sendall(message.encode('utf-8'))
            data = s.recv(1024).decode()
            if data == 'stop':
                break
            print(f"Server: {data}")
