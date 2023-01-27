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

left_vel =0
right_vel =0
PI=math.pi
py_serial = serial.Serial(
    # Window
    port='/dev/ttyACM0',
    # 보드 레이트 (통신 속도)
    baudrate=115200,
)
py_serial2 = serial.Serial(
    # Window
    port='/dev/ttyACM1',
    # 보드 레이트 (통신 속도)
    baudrate=115200,
)
    
HOST = '127.0.0.1'
PORT = 8000
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def send(s,S):
    c = int(s + S)
    munja =f's{s}\r\nS{S}\r\n c{c}\r\n'
    py_serial.write(munja.encode())
    print(munja)
#########################################
def go(s, S):
    global left_vel
    global right_vel
    left_vel, right_vel = s, S


# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        global data
        data = client_socket.recv(1024)

        print("recive : ",repr(data.decode()))
        
def read_from_arduino2():
    global left_vel
    global right_vel
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

    global fleft_vel_dodge
    global fright_vel_dodge
    global bleft_vel_dodge
    global bright_vel_dodge

    global target_x
    global target_y
    
    awef = True

    recieved_fl = False
    recieved_fr = False
    recieved_bl = False
    recieved_br = False

    if data != None:
        print(target_x, target_y)
        commend = data.decode()
        text= response.decode()
        m=[float(s) for s in re.findall(r'-?\d+\.?\d*', text)]#문자열에서 숫자추출
        if 'LL' in commend:
            fleft_vel_dodge = int(commend.split('LL')[1].split('  ')[0])
            recieved_fl = True
            awef = False
        else:
            recieved_fl = False
            awef = True

        if 'RR' in commend:
            fright_vel_dodge = int(commend.split('RR')[1].split('  ')[0])
            recieved_fr = True
            awef = False
            
        else:
            recieved_fr = False
            awef = True
        
        if 'XX' in commend:
            target_x = int(commend.split('XX')[1].split('  ')[0])
            awef = False
        else:
            awef = True
        if 'YY' in commend:
            target_y = int(commend.split('YY')[1].split('  ')[0])
            awef = False
        else:
            awef = True
            
        if left_vel + right_vel >= 0:
            if recieved_fl and recieved_fr and (not recieved_bl) and (not recieved_br) and (fright_vel_dodge > 0 or fleft_vel_dodge > 0):
                # print(f'front-> l : {fleft_vel_dodge}, r : {fright_vel_dodge}')
                go(1.2*fright_vel_dodge-0.8*fleft_vel_dodge, 1.2*fleft_vel_dodge-0.8*fright_vel_dodge)
                

        else:
            if recieved_bl and recieved_br and (not recieved_fl) and (not recieved_fr) and(bright_vel_dodge > 0 or bleft_vel_dodge > 0):
                # print(f'back-> l : {bleft_vel_dodge}, r : {bright_vel_dodge}')
                go(1.2*bright_vel_dodge-0.8*bleft_vel_dodge, 1.2*bleft_vel_dodge-0.8*bright_vel_dodge)
                
            
            



        if len(m) == 5:
            
            now_x, now_y=m[2],m[3]
            now_theta=m[4]
            
            if target_x - now_x == 0:
                if target_y-now_y < 0:
                    target_theta = -90
                elif target_y-now_y > 0:
                    target_theta = 90
                else:
                    target_theta = 0
            else:
                target_theta=math.atan((target_y-now_y)/(target_x-now_x))*180/PI#각도구하기 '도'
            reset_degree = float(360)
            if now_theta > reset_degree:
                for i in range(int((now_theta)/reset_degree)):
                    now_theta = now_theta-reset_degree*(i+1)
            elif now_theta < -reset_degree:
                for i in range(int((now_theta)/(-reset_degree))):
                    now_theta = now_theta+reset_degree*(i+1)
            
            dist = ((((target_x-now_x)**2)+((target_y-now_y)**2))**(1/2))
            # print(target_theta - now_theta)
            if ((target_x-now_x)<0):
                if dist >5:
                    if ((target_theta-now_theta-180)<-5):
                        if sig != 1:
                            go(0,0)
                            time.sleep(0.4)
                            go(-10, 10)
                            sig = 1
                        else:
                            print("rrr")
                    elif((target_theta-now_theta-180)>5):
                        if sig != 2:
                            go(0,0)
                            time.sleep(0.4)
                            go(10, -10)
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
            elif((target_x-now_x)>=0):
                if dist >5:
                    if ((target_theta-now_theta)>5):
                        if sig != 1:
                            go(0,0)
                            time.sleep(0.4)
                            go(10, -10)
                            sig = 1
                        else:
                            print("rrr")
                    elif((target_theta-now_theta)<-5):
                        if sig != 2:
                            go(0,0)
                            time.sleep(0.4)
                            go(-10, 10)
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
    time.sleep(2)
    while True:
            target_odo_move()
            send(left_vel, right_vel)
        # print(response)

client_socket.close()