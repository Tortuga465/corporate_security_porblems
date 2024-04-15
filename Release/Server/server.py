from socket import *
import rsa
import pickle


class TcpServer:
    def __init__(self):                                   
        self.ip = "127.0.0.1"                               # IPv4
        self.port = 12345                                   # Порт
        self.serv_pub = None                                # Открытый ключ сервера
        self.serv_priv = None                               # Закрытый ключ сервера
        self.client_pub = None                              # Открытый ключ клиента


    def start(self):                                   
        self.server = socket(AF_INET, SOCK_STREAM)          # IPv4 и TCP-сокет
        print("Сервер запущен")
        self.server.bind((self.ip, self.port))              # Привязка сокета к IP-адресу и порту
        self.server.listen(5)                               # Количество входящих соединений в очереди
        print("Ожидание входящий соединений")
        self.user, self.addr = self.server.accept()         # Принятие входящего соединения
        print(f"Соединение установлено с \n\t{self.addr}")
        

    def generate_keys(self):                                # Генерация и обмен ключей
        (self.serv_pub, self.serv_priv) = rsa.newkeys(2048)
        self.data = self.user.recv(4096)
        self.client_pub = pickle.loads(self.data)
        self.data = pickle.dumps(self.serv_pub)
        self.user.sendall(self.data)


    def communicate(self):
        while True:
            self.data = self.user.recv(4096)                                    # Получаем данные от клиента
            self.message = self.data                                            # Преобразуем байты в строку
            print(f"Шифрованное сообщение клиента: {self.message}")
            self.message = rsa.decrypt(self.message, self.serv_priv)
            self.message = self.message.decode("utf-8")
            if self.message == 'bye':
                break
            else:
                print(f"Расшифрованное сообщение клиента: {self.message}")
                self.message = self.message[::-1]                                   # Инвертируем строку клиента
                self.message = rsa.encrypt(self.message.encode("utf-8"), self.client_pub)
                self.user.send(self.message)                                        # Отправляем сообщение клиенту

    def stop(self):                                                         # Выключаем сервак
        self.server.close()                            
        print("Сервер выключен!")

s = TcpServer()
s.start()
s.generate_keys()
s.communicate()
s.stop()