import socket
import os

# настройка получателя, пользователь вводит адрес и порт сервера
server_ip = str(input(please enter the server address:)) 
server_port = int(input(please enter the server port:))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, server_port))

print("connected")

def send_file(filename):
    filesize = os.path.getsize(filename)

    # Отправка команды и имени файла
    s.sendall(f"FILE:{filename}".encode())

    # Отправка размера файла
    s.sendall(str(filesize).encode())

    # Чтение и отправка файла
    with open(filename, "rb") as f:
        bytes_read = f.read(filesize)
        s.sendall(bytes_read)
    print(f"File {filename} sent")

while True:
    message = input("massege or file: ")
    
    if message == "exit":
        s.sendall(message.encode())
        print("disconnection...")
        break
    elif os.path.isfile(message):
        send_file(message)
    else:
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        print(f"answer: {response}")

s.close()
