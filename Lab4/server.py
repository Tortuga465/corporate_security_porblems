import socket
from writeToFile import writeKey
from rsaModule import callable
from rsaModule import encrypt
from rsaModule import decrypt


HOST = "127.0.0.1"          # Объявление адреса сервера. Данный аддрес = localhost
PORT = 8005                 # Объявление порта подключения

class Server:
    def __init__(self):
        
        public_key, private_key = callable()
        self.public_key = public_key
        self.private_key = private_key
        writeKey("serverPrivatekey.txt",self.private_key)
        writeKey("serverPublickey.txt",self.public_key)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Добавление функционала, связанным с сокетами
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       # Добавление разрешения на повторное использование сокета. Упрощает жизнь при перезагрузке сервера
        self.socket.bind((HOST, PORT))                                          # Связка объекта socket с локальной конечной точкой
        self.socket.listen()                                                    # Начало прослушивания всех входящих запросов
        print(f"Server is running on address {HOST} and port {PORT}. Awaiting connection")
        conn, addr = self.socket.accept()                                       # Ожидание подключения
        self.conn = conn                                                        # Добавление переменной в объект
        self.addr = addr                                                        # Добавление переменной в объект
        self.conn.send(bytes((str(self.public_key)), encoding='UTF-8'))
        self.public_key_client=self.conn.recv(2048)
        
        self.pk=(int(self.private_key[0]),int (self.private_key[1]))



    def __enter__(self):
        return self
    
    def mainloop(self):        
        # conn, addr = self.socket.accept()                                    
        data = self.conn.recv(2048)                                             # Ожидание входящего сообщения определенной длины
        if data:
            data_decoded=str(data, encoding='UTF-8')                                # Расшифровка полученного сообщения
            # print(data_decoded)                                                     # Отображение полученного сообщения в консоли сервера
            data_decoded=data_decoded.split()
            data_decoded[0]=(data_decoded[0][1:-1])
            print(data_decoded)                                                     # Отображение полученного сообщения в консоли сервера
            for i, item in enumerate( data_decoded):
                data_decoded[i]=int(data_decoded[i][1:-1])
            print("Encrypted message is ", data_decoded)
            decrypt(self.pk, data_decoded)
            # print(decrypt(self.private_key, data_decoded))
            # if(data_decoded!='exit'):   
            #     self.conn.send(bytes('Hello from server!', encoding='UTF-8'))       # Отправка сообщения клиенту     
        else:
            return

    def __exit__(self, exc_type, exc_val, exc_tb):                              # Завершение работы сервера
        self.socket.shutdown(socket.SHUT_RDWR)                                  # Выключение передачи данных в сокете
        self.socket.close()                                                     # Закрытие сокета


if __name__ == '__main__':                                                      # Цикл работы
    with Server() as app:
        while True:
            app.mainloop()                                  




