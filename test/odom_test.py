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
############

target_x = 0
target_y = 0
sig = 0
now_x = 0
now_y = 0

left_vel = 0
right_vel = 0

fleft_vel_dodge = 0
fright_vel_dodge = 0
bleft_vel_dodge = 0
bright_vel_dodge = 0

PI=math.pi
py_serial = serial.Serial(
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

#########################################

def send(s,S):
    munja =f's{s}  S{S}'
    py_serial.write(munja.encode())
    time.sleep(0.1)
#########################################

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True:
        global data
        data = client_socket.recv(1024)

        print("receive : ",repr(data.decode()))
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

def read_from_arduino():
    while True:
        global left_vel
        global right_vel
        global response
        if py_serial.readable():
            response = py_serial.readline()
        #b's:  0.00     S:  0.00     nowx:  0.00     nowy:  0.00     now_theta:  0.00\r\n'
        print(response)
        target_odo_move()
        send(left_vel, right_vel)

def go(s, S):
    global left_vel
    global right_vel
    left_vel, right_vel = s, S



def target_odo_move():
    print('is in')
    global response
    global sig
    global data

    global left_vel
    global right_vel

    global fleft_vel_dodge
    global fright_vel_dodge
    global bleft_vel_dodge
    global bright_vel_dodge

    recieved_fl = False
    recieved_fr = False
    recieved_bl = False
    recieved_br = False

    noerr = False

    # if py_serial.readable():
    #     response = py_serial.readline()
    # print(response)

    if data != None:
        commend = data.decode()
        text= response.decode()
        m=[float(s) for s in re.findall(r'-?\d+\.?\d*', text)]#문자열에서 숫자추출
        print(commend)
        if 'FL' in commend:
            fleft_vel_dodge = int(commend.split('FL')[1].split('  ')[0])
            recieved_fl = True
        else:
            fleft_vel_dodge = 0
            recieved_fl = False

        if 'FR' in commend:
            fright_vel_dodge = int(commend.split('FR')[1].split('  ')[0])
            recieved_fr = True

        else:
            fright_vel_dodge = 0
            recieved_fr = False

        if 'BL' in commend:
            bleft_vel_dodge = int(commend.split('BL')[1].split('  ')[0])
            recieved_bl = True
        else:
            bleft_vel_dodge = 0
            recieved_bl = False

        if 'BR' in commend:
            bright_vel_dodge = int(commend.split('BR')[1].split('  ')[0])
            recieved_br = True

        else:
            bright_vel_dodge = 0
            recieved_br = False

        if recieved_fl and recieved_fr and recieved_bl and recieved_br:
            noerr = True


        if len(m) == 5:
            now_x, now_y=m[2],m[3]
            now_theta=m[4]

            ta=[float(tas) for tas in re.findall(r'-?\d+\.?\d*', commend)]#문자열에서 숫자추출

            if (len(ta) == 2) and noerr:
                target_x,target_y = ta[0],ta[1]
                target_theta=math.atan((target_y-now_y)/(target_x-now_x))*180/PI#각도구하기 '도'
                dist = ((((target_x-now_x)**2)+((target_y-now_y)**2))**(1/2))
                #######################################
                reset_degree = float(360)
                if now_theta > reset_degree:
                    for i in range(int((now_theta)/reset_degree)):
                        now_theta = now_theta-reset_degree*(i+1)
                elif now_theta < -reset_degree:
                    for i in range(int((now_theta)/(-reset_degree))):
                        now_theta = now_theta+reset_degree*(i+1)

                # 뒤로가기
                if ((target_x-now_x)<0):
                    if dist >5:
                        if ((target_theta-now_theta)>5):
                            if sig != 1:
                                go(0,0)
                                time.sleep(0.4)
                                go(20, -20)
                                sig = 1
                            else:
                                print("rrr")
                        elif((target_theta-now_theta)<-5):
                            if sig != 2:
                                go(0,0)
                                time.sleep(0.4)
                                go(-20,20)
                                sig = 2
                            else:
                                print("lll")
                        else:
                            if sig != 3:
                                go(-20-bleft_vel_dodge, -20-bright_vel_dodge)
                                sig = 3
                            else:
                                print("ggg")
                    else:
                            if sig != 4:
                                go(0, 0)
                                sig = 4
                            else:
                                print("ststst")

                # 앞으로가기
                elif((target_x-now_x)>=0):
                    if dist >5:
                        if ((target_theta-now_theta)>5):
                            if sig != 1:
                                go(0,0)
                                time.sleep(0.4)
                                go(20,-20)
                                sig = 1
                            else:
                                print("rrr")
                        elif((target_theta-now_theta)<-5):
                            if sig != 2:
                                go(0,0)
                                time.sleep(0.4)
                                go(-20, 20)
                                sig = 2
                            else:
                                print("lll")
                        else:
                            if sig != 3:
                                go(20+fleft_vel_dodge, 20+fright_vel_dodge)
                                sig = 3
                            else:
                                print("ggg")
                    else:
                            if sig != 4:
                                go(0, 0)
                                sig = 4
                            else:
                                print("ststst")

            # elif(len(ta) == 3):
            #         arco_x, arco_y, arco_t = ta[0], ta[1], ta[2]
            #         now_munja=f'x {arco_x} y {arco_y} t {arco_t}'
            #         py_serial.write(now_munja.encode())

if __name__ == "__main__":

    #
    while True:
        thread1 = threading.Thread(target=read_from_arduino, daemon=True)
        #thread2 = threading.Thread(target=target_odo_move, daemon=True)
        thread1.start()
        #thread2.start()
        #target_odo_move()
        thread1.join(timeout = 1)
        #thread2.join()


client_socket.close()
