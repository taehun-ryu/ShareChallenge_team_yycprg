import os
import ydlidar
import time
import sys
import numpy as np
import math
import socket
from _thread import *

HOST = '127.0.0.1'
PORT = 8000
data = None
data_sig = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

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

#################################
def recv_data(client_socket) :
    while True :
        global data
        data = client_socket.recv(1024)

        print("recive : ",repr(data.decode()))
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')



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
                   # 측정 각도 제한.
                   if 0<= new_angle_left and new_angle_left <= left_rad:
                       angle = np.append(angle,new_angle_left)
                       ran=np.append(ran,point.range)
                   elif right_rad<new_angle_right and new_angle_right<0:
                       angle = np.append(angle,new_angle_right)
                       ran=np.append(ran,point.range)
        front_angle = angle
        front_ran = ran
        front_size = len(front_angle)

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
                    angle = np.append(angle,-point.angle)
                    ran = np.append(ran,point.range)
        else:
            for point in back_scan.points:
                if point.range > 0 and point.range < limit and (-point.angle >left_rad or -point.angle < right_rad):
                    angle = np.append(angle,-point.angle)
                    ran = np.append(ran,point.range)
        back_angle = angle
        back_ran = ran
        back_size=len(back_angle)

# Polar coordinate system -> Cartesian coordinate system
def changeToXY(ran,angle,size):
    x = np.array([])
    y = np.array([])
    for i in range(size):
        x = np.append(x,ran[i] * math.cos(angle[i]))
        y = np.append(y,ran[i] * math.sin(angle[i]))
    return x,y


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
            front_x, front_y = changeToXY(front_ran,front_angle,front_size)
            back_x, back_y = changeToXY(back_ran,back_angle,back_size)


            # Local Plan using Lidar
            front_right_circle = (front_x+0.4)**2+(front_y+0.3)**2
            front_left_circle = (front_x+0.4)**2+(front_y-0.3)**2

            back_right_circle = (back_x-0.2)**2+(back_y+0.3)**2
            back_left_circle = (back_x-0.2)**2+(back_y-0.3)**2

            if data != None:
                # front
                if np.any(front_right_circle < (0.85)**2 ) and np.any(front_left_circle < (0.85)**2) and np.any(front_y<-0.5) and np.any(front_y>0.5):
                    if data_sig != 2:
                        print("bbb")
                        client_socket.send('fb'.encode())
                        data_sig = 2

                elif np.any(front_right_circle < (0.85)**2) and np.any(front_left_circle > (0.85)**2) and np.any(front_y<-0.5) and np.any(front_y>0.5) :
                    if data_sig != 4:
                        print("llll")
                        client_socket.send('fl'.encode())
                        data_sig = 4

                elif np.any(front_right_circle > (0.85)**2) and np.any(front_left_circle < (0.85)**2) and np.any(front_y<-0.5) and np.any(front_y>0.5):
                    if data_sig != 3:
                        print("rrrr")
                        client_socket.send('fr'.encode())
                        data_sig = 3

                # target
                else:
                    if data_sig != 1:
                        client_socket.send(data)
                        data_sig = 1
                    else:
                        pass


        ret1 = laser_front.turnOff()
        ret2 = laser_back.turnOff()

    laser_front.disconnecting()
    laser_back.disconnecting()
