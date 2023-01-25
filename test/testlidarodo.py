import os
import ydlidar
import time
import sys
import numpy as np
import math
import socket
from _thread import *
import select
import serial
import re
import serial
import time
import traceback
import threading
############
RMAX = 32.0

port1 = "/dev/ttyUSB1"
port2 = "/dev/ttyUSB0"

laser_front = ydlidar.CYdLidar()
laser_front.setlidaropt(ydlidar.LidarPropSerialPort, port1)
laser_front.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
laser_front.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser_front.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser_front.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
laser_front.setlidaropt(ydlidar.LidarPropSampleRate, 9)
laser_front.setlidaropt(ydlidar.LidarPropSingleChannel, False)

laser_back = ydlidar.CYdLidar()
laser_back.setlidaropt(ydlidar.LidarPropSerialPort, port2)
laser_back.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
laser_back.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser_back.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser_back.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
laser_back.setlidaropt(ydlidar.LidarPropSampleRate, 9)
laser_back.setlidaropt(ydlidar.LidarPropSingleChannel, False)
############odometry

target_x = 0
target_y = 0
sig = 0

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

def read_from_arduino():
    global response
    while True:
        if py_serial.readable():
            response = py_serial.readline()
            print(response)
        else:
            pass

thread1 = threading.Thread(target=read_from_arduino, daemon=True)
thread1.start()



#########################################

def go(s,S):
    munja =f's{s}  S{S}'
    py_serial.write(munja.encode())
#########################################
# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        global data
        data = client_socket.recv(1024)

        #print("recive : ",repr(data.decode()))
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')



def target_odo_move():
    global response
    global sig
    if data != None:
        commend = data.decode()
        ta=[float(tas) for tas in re.findall(r'-?\d+\.?\d*', commend)]#문자열에서 숫자추출
        target_x,target_y = ta[0],ta[1]
        text= response.decode()
        m=[float(s) for s in re.findall(r'-?\d+\.?\d*', text)]#문자열에서 숫자추출
        now_x, now_y=m[2],m[3]
        #######################################
        target_theta=math.atan((target_y-now_y)/(target_x-now_x))*180/PI#각도구하기 '도'
        now_theta=m[4]
        if now_theta > 360:
            now_theta = now_theta-360
        elif now_theta < -360:
            now_theta = now_theta +360
        dist = ((((target_x-now_x)**2)+((target_y-now_y)**2))**(1/2))
        if ((target_x-now_x)<0):
            if dist >5:
                print((target_theta-now_theta-180))
                if ((target_theta-now_theta-180)<-5):
                    if sig != 1:
                        go(0,0)
                        time.sleep(0.4)
                        go(-20,20)
                        sig = 1
                    else:
                        print("rrr")
                elif((target_theta-now_theta-180)>5):
                    if sig != 2:
                        go(0,0)
                        time.sleep(0.4)
                        go(20, -20)
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
        else: 
                if sig != 4:
                    go(0, 0)
                    sig = 4
                else:
                    print("ststst")


############odometry
# 전방 라이다 sensing
# type: True -> 스캔 각도 제한
# limit -> 스캔 거리 제한.
def receiveLidarValue_front(type:bool=True,limit:float=None):
    global front_size , front_angle, front_ran
    r = laser_front.doProcessSimple(front_scan)

    if type:
        left_rad = 1.73
        right_rad = -1.74
    else:
        left_rad = math.pi
        right_rad = -math.pi

    if r:
        angle=np.array([])
        ran=np.array([])
        front_size = 0
        if limit is None:
            for point in front_scan.points:
               new_angle_left = -(point.angle - math.pi)
               new_angle_right = -(point.angle + math.pi)
               # 최대 측정 거리를 넘어가면 range를 0으로 반환함.
               if point.range > 0:
                   front_size+=1
                   # 측정 각도 제한.
                   if 0<= new_angle_left and new_angle_left <= left_rad:
                       angle = np.append(angle,new_angle_left)
                       ran=np.append(ran,point.range)
                   elif right_rad<new_angle_right and new_angle_right<0:
                       angle = np.append(angle,new_angle_right)
                       ran=np.append(ran,point.range)
        else:
            for point in front_scan.points:
               new_angle_left = -(point.angle - math.pi)
               new_angle_right = -(point.angle + math.pi)
               # 최대 측정 거리를 넘어가면 range를 0으로 반환함.
               if point.range > 0 and point.range < limit:
                   front_size+=1
                   # 측정 각도 제한.
                   if 0<= new_angle_left and new_angle_left <= left_rad:
                       angle = np.append(angle,new_angle_left)
                       ran=np.append(ran,point.range)
                   elif right_rad<new_angle_right and new_angle_right<0:
                       angle = np.append(angle,new_angle_right)
                       ran=np.append(ran,point.range)
        front_angle = angle
        front_ran = ran

# 후방 라이다 sensing     
def receiveLidarValue_back(type:bool=True,limit:float=None):
    global back_size, back_angle, back_ran
    r = laser_back.doProcessSimple(back_scan)
    if type:
        left_rad = 1.4
        right_rad = -1.7
    else:
        left_rad = 0
        right_rad = 0

    if r:
        angle = np.array([])
        ran = np.array([])
        back_size = 0
        if limit is None:
            for point in back_scan.points:
                if point.range > 0 and (-point.angle >left_rad or -point.angle < right_rad):
                    back_size +=1
                    angle = np.append(angle,-point.angle)
                    ran = np.append(ran,point.range)
        else:
            for point in back_scan.points:
                if point.range > 0 and point.range < limit and (-point.angle >left_rad or -point.angle < right_rad):
                    back_size +=1
                    angle = np.append(angle,-point.angle)
                    ran = np.append(ran,point.range)
        back_angle = angle
        back_ran = ran

# r,theta -> x,y 변환.
def changeToXY():
    global front_size
    x = np.array([])
    y = np.array([])
    for i in range(front_size):
        x = np.append(x,front_ran[i] * math.cos(front_angle[i]))
        y = np.append(y,front_ran[i] * math.sin(front_angle[i]))
    return x,y

# weighted sum 방식을 이용한 planning
def front_weight_sum():
    front_r_theta = np.stack((front_ran,front_angle),axis = 1)
    front_ran_sort = np.sort(front_ran)
    front_ran_argsort = np.argsort(front_ran)
    


if __name__ == '__main__':
    ret1 = laser_front.initialize()
    ret2 = laser_back.initialize()

    if ret1 or ret2:
        ret1 = laser_front.turnOn()
        ret2 = laser_back.turnOn()

        front_scan = ydlidar.LaserScan()
        back_scan = ydlidar.LaserScan()

        while ret1 and ret2 and ydlidar.os_isOk():
            receiveLidarValue_front()
            receiveLidarValue_back()
            front_weight_sum()
            front_ran = np.where(front_ran>=3,3,front_ran)
            t = np.sum(front_ran*front_angle)
            
            
            if data != None:
                try:
                    commend = data.decode()
                    ta=[float(tas) for tas in re.findall(r'-?\d+\.?\d*', commend)]#문자열에서 숫자추출
                    target_x,target_y = ta[0],ta[1]
                    text= response.decode()
                    m=[float(s) for s in re.findall(r'-?\d+\.?\d*', text)]#문자열에서 숫자추출
                    now_x, now_y=m[2],m[3]
                    #######################################
                    target_theta=math.atan((target_y-now_y)/(target_x-now_x))*180/PI#각도구하기 '도'
                    now_theta=m[4]
                    if now_theta > 360:
                        now_theta = now_theta-360
                    elif now_theta < -360:
                        now_theta = now_theta +360
                    dist = ((((target_x-now_x)**2)+((target_y-now_y)**2))**(1/2))
                except:
                    print(data)
                    print('is the error data')
            
            
            if np.sum(front_ran)<=450:
                if np.sum(front_ran)<=310:
                    go(-20,-20)
                else:
                    if t <0:
                        go(0, 20)
                    else:
                        go(20, 0)
            else:
                target_odo_move()

        ret1 = laser_front.turnOff()
        ret2 = laser_back.turnOff()

    laser_front.disconnecting()
    laser_back.disconnecting()

client_socket.close()