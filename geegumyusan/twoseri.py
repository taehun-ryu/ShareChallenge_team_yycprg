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
    # Window
    port='/dev/ttyUSB2',
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

        #print("recive : ",repr(data.decode()))
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
    global left_vel  
    global right_vel

    global left_vel_dodge
    global right_vel_dodge
    if data != None:
        commend = data.decode()
        text= response.decode()
        m=[float(s) for s in re.findall(r'-?\d+\.?\d*', text)]#문자열에서 숫자추출
        print(len(m))
        if len(m) == 5:
            now_x, now_y=m[2],m[3]
            now_theta=m[4]

            if commend == 'l':

                if sig != 5:
                    go(20,5)
                    sig = 5
            elif commend == 'r':
                if sig != 6:
                    go(5,20)
                    sig = 6
            elif commend == 'b':
                if sig != 7:
                    go(-20,-20)
                    sig = 7

            else:
                ta=[float(tas) for tas in re.findall(r'-?\d+\.?\d*', commend)]#문자열에서 숫자추출
                target_x,target_y = ta[0],ta[1]
                #######################################
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

                if ((target_x-now_x)<0):
                    if dist >5:
                        if ((target_theta-now_theta)>5):
                            if sig != 1:
                                go(0,0)
                                time.sleep(0.4)
                                go(0, -20)
                                sig = 1
                            else:
                                print("rrr")
                        elif((target_theta-now_theta)<-5):
                            if sig != 2:
                                go(0,0)
                                time.sleep(0.4)
                                go(-20, 0)
                                sig = 2
                            else:
                                print("lll")
                        else:
                            if sig != 3:
                                go(-20, -20)
                                sig = 3
                            else:
                                print("ggg")
                    else:
                            if sig != 4:
                                go(0, 0)
                                sig = 4
                            else:
                                print("ststst")
                elif((target_x-now_x)>=0):
                    if dist >5:
                        if ((target_theta-now_theta)>5):
                            if sig != 1:
                                go(0,0)
                                time.sleep(0.4)
                                go(20, 0)
                                sig = 1
                            else:
                                print("rrr")
                        elif((target_theta-now_theta)<-5):
                            if sig != 2:
                                go(0,0)
                                time.sleep(0.4)
                                go(0, 20)
                                sig = 2
                            else:
                                print("lll")
                        else:
                            if sig != 3:
                                go(20, 20)
                                sig = 3
                            else:
                                print("ggg")
                    else:
                            if sig != 4:
                                go(0, 0)
                                sig = 4
                            else:
                                print("ststst")
# def read_from_arduino():
#     global response
#     while True:
#         if py_serial.readable():
#             response = py_serial.readline()
#             print(response)
#         else:
#             pass
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

thread2 = threading.Thread(target=read_from_arduino2, daemon=True)
thread2.start()
# thread1 = threading.Thread(target=read_from_arduino, daemon=True)
# thread1.start()
if __name__ == "__main__":

    while True:
            target_odo_move()
        # print(response)

client_socket.close()