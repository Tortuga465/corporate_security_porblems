import socket

HOST = "127.0.0.1"          # Объявление адреса сервера. Данный аддрес = localhost
PORT = 8005                 # Объявление порта подключения

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))    # Связка объекта socket с локальной конечной точкой
    s.listen()              # Начало прослушивания всех входящих запросов
    print(f"Server is running on address {HOST} and port {PORT}. Awaiting connection")
    
    
    while True:
        conn, addr = s.accept()                                     # Ожидание подключения
        data = conn.recv(1024)                                      # Ожидание входящего определенной длины
        print(str(data))                                            # Отображение полученного сообщения в консоли сервера
        conn.send(bytes('Hello from server!', encoding='UTF-8'))    # Отправка сообщения клиенту
        conn.close()                                                # Закрытие соединения