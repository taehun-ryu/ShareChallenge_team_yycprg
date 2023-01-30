import socket
from _thread import *
import select
import sys
import serial
import time
import math
import re
import serial
import time
import traceback
import threading

target_x = 0
target_y = 0
sig = 0

PI=math.pi
py_serial = serial.Serial(
    # arduino port
    port='/dev/ttyACM1',
    # 보드 레이트 (통신 속도)
    baudrate=115200,
)
py_serial2 = serial.Serial(
    # Window
    port='/dev/ttyACM0',
    # 보드 레이트 (통신 속도)
    baudrate=115200,
)
    
HOST = '127.0.0.1'
PORT = 8000
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def go(s,S):
    munja =f's{s}\r\nS{S}\r\n'
    py_serial.write(munja.encode())
#########################################
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        global data
        data = client_socket.recv(1024)

        print("recive : ",repr(data.decode()))

def read_from_arduino2():
    global response
    while True:
        if py_serial2.readable():
            response = py_serial2.readline()
            print(response)
        else:
            pass

def target_odo_move():
    global response
    global sig
    global data

    global left_vel_dodge
    global right_vel_dodge
    global while_sig, flag, flag_time

    if data != None:
        commend = data.decode()
        text= response.decode()
        m=[float(s) for s in re.findall(r'-?\d+\.?\d*', text)]#문자열에서 숫자추출
        #print(len(m))
        if len(m) == 5:
            now_x, now_y=m[2],m[3]
            now_theta=m[4]

            ta=[float(tas) for tas in re.findall(r'-?\d+\.?\d*', commend)]#문자열에서 숫자추출

            target_x, target_y, left_vel, right_vel,front_disCm, back = ta[0],ta[1],ta[2],ta[3],ta[4],ta[5]
            print(f'{target_x} {target_y} {left_vel},{right_vel},{front_disCm},{back}')

            if target_x - now_x == 0:
                if target_y-now_y < 0:
                    target_theta = -90
                elif target_y-now_y > 0:
                    target_theta = 90
                else:
                    target_theta = 0
            else:
                target_theta=math.atan((target_y-now_y)/(target_x-now_x))*180/PI#각도구하기 '도'
            if now_theta > 360:
                for i in range(int((now_theta)/360)):
                    now_theta = now_theta-360*(i+1)
            elif now_theta < -360:
                for i in range(int((now_theta)/(-360))):
                    now_theta = now_theta+360*(i+1)

            dist = ((((target_x-now_x)**2)+((target_y-now_y)**2))**(1/2))

            if front_disCm <=25:
                if sig!=5:
                    go(0,0)
                    sig = 5
                else:
                    print("Too Close")
            if dist > 100:
                print("장애물 회피하면서 타깃 좌표로 스스로 이동하는거 보여주면 좋음")

            # 장애물 피할 일이 있ㅇㄹ까 싶음 
            elif dist>10:
                if ((target_theta-now_theta)>7):
                    if sig != 1:
                        go(20,-20)
                        sig = 1
                    else:
                        print("rrr")
                elif((target_theta-now_theta)<-7):
                    if sig != 2:
                        go(-20, 20)
                        sig = 2
                    else:
                        print("lll")
                else:
                    if sig != 3:
                        go(20, 20)
                        sig = 3
                    else:
                        print("타깃 직전")
            else:
                if sig !=4:
                    go(0,0)
                    sig = 4
                else:
                    print("타깃 도착")

start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

thread2 = threading.Thread(target=read_from_arduino2, daemon=True)
thread2.start()
# thread1 = threading.Thread(target=read_from_arduino, daemon=True)
# thread1.start()
if __name__ == "__main__":
    while_sig = True
    flag = False
    flag_time = 0
    while True:
            target_odo_move()
        # print(response)

client_socket.close()