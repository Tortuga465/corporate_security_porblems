import socket

HOST = "127.0.0.1"          # Объявление адреса сервера. Данный аддрес = localhost
PORT = 8005                     # Объявление порта подключения


class Application:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.bind((HOST, PORT))                                        # Связка объекта socket с локальной конечной точкой
        # self.socket.connect((HOST, PORT))                                                 # Подключение клиента к серверу по указанному адресу и порту
        self.socket.connect((HOST, PORT))                                                 # Подключение клиента к серверу по указанному адресу и порту
        self.server_public_key = self.socket.recv(2048)                                                     # Получение данных (сообщение) от сервера
        print(self.server_public_key)
        
    def __enter__(self):
        return self

    def mainloop(self):
        
        message=""                                                              # Объявление переменной сообщения, которое отправит клиент
        while True:

            # data = self.socket.recv(2048)                                                     # Получение данных (сообщение) от сервера
            # print(f"{data}")                                             # Печать сообщения, полученного от сервера
            message=input("Enter message to send to server ")        # Пользователь вводит сообщение, которое он хочет отправить серверу
            self.socket.sendall(bytes(message, "UTF-8"))                                                      # Клиент отправляет сообщение серверу
            if message=="exit":
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()            
                break
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

if __name__ == '__main__':
    with Application() as app:
        while True:
            app.mainloop()