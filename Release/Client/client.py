from socket import * 
import rsa
import pickle

class TcpClient:
    def __init__(self):
        self.ip = "127.0.0.1"                                       # IPv4
        self.port = 12345                                           # Порт
        self.client_pub = None                                      # Открытый ключ клиента
        self.client_priv = None                                     # Закртый ключ клиента
        self.serv_pub = None                                        # Открытый ключ сервера
        
    def start(self):
        self.client = socket(AF_INET, SOCK_STREAM)                  # IPv4 и TCP-сокет
        self.client.connect((self.ip,self.port))                    # Подключаемся к серверу
        print("Подключение выполнено")

    def generate_keys(self):                                        # Генерация и обмен ключей
        (self.client_pub, self.client_priv) = rsa.newkeys(2048)
        self.data = pickle.dumps(self.client_pub)
        self.client.sendall(self.data)
        self.data = self.client.recv(4096)
        self.serv_pub = pickle.loads(self.data)

    def communicate(self):
        while True:
            self.message = input("Введите сообщение: ")
            if self.message == 'bye':
                self.message = rsa.encrypt(self.message.encode("utf-8"), self.serv_pub)   
                self.client.send(self.message)    
                break
            else:
                self.message = rsa.encrypt(self.message.encode("utf-8"), self.serv_pub)   
                self.client.send(self.message)                              # Отправляем сообщение серверу
                self.data = self.client.recv(4069)                          # Получаем данные с сервера
                print("Шифрованное сообщение сервера: ", self.data)
                self.data = rsa.decrypt(self.data, self.client_priv)
                self.message = self.data.decode("utf-8")
                print("Расшифрованное сообщение сервера: ", self.message)


    def stop(self):                                                 # Закрытие сокета
        self.client.close()
        print("Клиент выключен!")

c = TcpClient()
c.start()
c.generate_keys()
c.communicate()
c.stop()