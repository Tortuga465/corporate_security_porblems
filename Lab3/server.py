import socket
from rsaModule import callable

HOST = "127.0.0.1"          # Объявление адреса сервера. Данный аддрес = localhost
PORT = 8005                 # Объявление порта подключения

class Application:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Добавление функционала, связанным с сокетами
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       # Добавление разрешения на повторное использование сокета. Упрощает жизнь при перезагрузке сервера
        self.socket.bind((HOST, PORT))                                          # Связка объекта socket с локальной конечной точкой
        self.socket.listen()                                                    # Начало прослушивания всех входящих запросов
        print(f"Server is running on address {HOST} and port {PORT}. Awaiting connection")
        conn, addr = self.socket.accept()                                       # Ожидание подключения
        self.conn = conn                                                        # Добавление переменной в объект
        self.addr = addr                                                        # Добавление переменной в объект



    def __enter__(self):
        return self
    
    def mainloop(self):        
        # conn, addr = self.socket.accept()                                    
        data = self.conn.recv(1024)                                             # Ожидание входящего сообщения определенной длины
        data_decoded=str(data, encoding='UTF-8')                                # Расшифровка полученного сообщения
        print(data_decoded)                                                     # Отображение полученного сообщения в консоли сервера
        if(data_decoded!='exit'):   
            self.conn.send(bytes('Hello from server!', encoding='UTF-8'))       # Отправка сообщения клиенту     


    def __exit__(self, exc_type, exc_val, exc_tb):                              # Завершение работы сервера
        self.socket.shutdown(socket.SHUT_RDWR)                                  # Выключение передачи данных в сокете
        self.socket.close()                                                     # Закрытие сокета


if __name__ == '__main__':                                                      # Цикл работы
    with Application() as app:
        while True:
            app.mainloop()                                  




    
    
