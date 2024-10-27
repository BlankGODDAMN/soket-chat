import socket
import os

# настройка получателя, пользователь вводит адрес и порт сервера
server_ip = str(input(please enter the server address:)) 
server_port = int(input(please enter the server port:))

# Создание сокета
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, server_port))
s.listen(1)

print("waiting for the connection...")

conn, addr = s.accept()
print(f"connected with: {addr}")

while True:
    data = conn.recv(1024).decode()
    
    if data == "exit":
        print("client has disconnected")
        break
    
    # Проверка, является ли сообщение командой для передачи файла
    if data.startswith("FILE:"):
        # Извлекаем только имя файла
        filename = os.path.basename(data[5:])  
        filesize = conn.recv(1024).decode()  # Получение размера файла
        filesize = int(filesize)

        # Прием файла
        with open(f"received_{filename}", "wb") as f:
            bytes_read = conn.recv(filesize)
            f.write(bytes_read)
        print(f"File {filename} received")
        conn.sendall(f"File {filename} received".encode())
    else:
        print(f"client says: {data}")
        response = input("your answer: ")
        conn.sendall(response.encode())

conn.close()
s.close()
