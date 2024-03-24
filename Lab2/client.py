import socket

HOST = "127.0.0.1"          # Объявление адреса сервера. Данный аддрес = localhost
PORT = 8005                     # Объявление порта подключения


class Application:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.bind((HOST, PORT))                                        # Связка объекта socket с локальной конечной точкой
        
    def __enter__(self):
        return self

    def mainloop(self):
        self.socket.connect((HOST, PORT))                                                 # Подключение клиента к серверу по указанному адресу и порту
        message=""                                                              # Объявление переменной сообщения, которое отправит клиент
        while True:
            message=input("Enter message to send to server ")        # Пользователь вводит сообщение, которое он хочет отправить серверу
            self.socket.sendall(bytes(message, "UTF-8"))                                                      # Клиент отправляет сообщение серверу
            if message=="exit":
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()            
                break
            data = self.socket.recv(1024)                                                     # Получение данных (сообщение) от сервера
            print(f"Received {data!r}")                                             # Печать сообщения, полученного от сервера
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

if __name__ == '__main__':
    with Application() as app:
        while True:
            app.mainloop()