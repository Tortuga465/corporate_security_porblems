import socket

from writeToFile import writeKey
from rsaModule import callable
from rsaModule import encrypt
from rsaModule import decrypt

HOST = "127.0.0.1"          # Объявление адреса сервера. Данный аддрес = localhost
PORT = 8005                     # Объявление порта подключения


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.bind((HOST, PORT))                                        # Связка объекта socket с локальной конечной точкой
        # self.socket.connect((HOST, PORT))                                                 # Подключение клиента к серверу по указанному адресу и порту
        self.socket.connect((HOST, PORT))                                                 # Подключение клиента к серверу по указанному адресу и порту
        public_key, private_key = callable()
        self.public_key = public_key
        self.private_key = private_key
        self.server_public_key = self.socket.recv(2048)                                                     # Получение данных (сообщение) от сервера
        data_decoded=str(self.server_public_key, encoding='UTF-8')
        data_decoded=data_decoded.split()
        for i, item in enumerate( data_decoded):
            data_decoded[i]=int(item[1:-1])
        self.public_key_server=data_decoded
        print(data_decoded)
        
        writeKey("clientPrivatekey.txt",self.private_key)
        writeKey("clientPublickey.txt",self.public_key)
        for item in self.public_key:
            # print(item)
            self.socket.sendall(bytes(str(item), "UTF-8"))

        
    def __enter__(self):
        return self

    def mainloop(self):
        
        message=""                                                              # Объявление переменной сообщения, которое отправит клиент
        while True:
            message=input("Enter message to send to server ")        # Пользователь вводит сообщение, которое он хочет отправить серверу
            message=encrypt(self.public_key_server, message)
            print ("Encrypted message: ",message)           
            message=message.join()
            self.socket.sendall(bytes(message, "UTF-8"))                                                      # Клиент отправляет сообщение серверу
            if message=="exit":
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()            
                break
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

if __name__ == '__main__':
    with Client() as app:
        while True:
            app.mainloop()