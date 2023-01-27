import socket
from _thread import *
import time

HOST = '127.0.0.1'
PORT = 8000
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 외부망
HOST2 = '127.0.0.1'
PORT2 = 8000
data2 = None
client_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket2.connect((HOST2, PORT2))

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket2) :
    while True :
        global data
        data = client_socket2.recv(1024)
        print("recive : ",repr(data.decode()))

start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

while True:
    message = data
    if message == 'quit':
        close_data = message
        break

    client_socket.send(message.encode())


client_socket.close()