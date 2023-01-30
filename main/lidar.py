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

HOST2 = '192.168.0.15'
PORT2 = 8001
data2 = None
client_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket2.connect((HOST2, PORT2))

port1 = "/dev/ttyUSB1"  # front_liudar port
port2 = "/dev/ttyUSB0"  # back_liudar port

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
def recv_data(client_socket2) :
    while True :
        global data2
        data2 = client_socket2.recv(1024)

        print("recive : ",repr(data2.decode()))
start_new_thread(recv_data, (client_socket2,))
print ('>> Connect Server')



# 전방 라이다 sensing
# type: True -> 스캔 각도 제한
# limit -> 스캔 거리 제한.
def receiveLidarValue_front(type:bool=False,limit:float=None):
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
def receiveLidarValue_back(type:bool=False,limit:float=None):
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

        left_vel = 0
        right_vel = 0

        back_obstacle = 0


        while ret1 and ret2 and ydlidar.os_isOk():
            receiveLidarValue_front(type=True)
            receiveLidarValue_back()

            front_x, front_y = changeToXY(front_ran,front_angle,front_size)
            back_x, back_y = changeToXY(back_ran,back_angle,back_size)

            front_ran_1 = np.where((front_ran>1),1,front_ran)

            left_0_1 = []
            left_1_2 = []
            left_2_3 = []

            right_0_1 = []
            right_1_2 = []
            right_2_3 = []

            back = []
            front = []

            point_angle = [75, 50, 25, -25, -50, -75]

            for j, i in zip(front_ran_1, front_angle):
                if i >= math.radians(point_angle[0]) or i <= math.radians(point_angle[5]):
                    continue

                if i >= math.radians(point_angle[5]) and i <= math.radians(point_angle[4]):
                    right_2_3.append(j)
                if i >= math.radians(point_angle[4]) and i <= math.radians(point_angle[3]):
                    right_1_2.append(j)
                if i >= math.radians(point_angle[3]) and i <= math.radians(-0.0):
                    right_0_1.append(j)

                if i >= math.radians(+0.0) and i <= math.radians(point_angle[2]):
                    left_0_1.append(j)
                if i >= math.radians(point_angle[2]) and i <= math.radians(point_angle[1]):
                    left_1_2.append(j)
                if i >= math.radians(point_angle[1]) and i <= math.radians(point_angle[0]):
                    left_2_3.append(j)
                if j < 0:
                    print('err')

            for i,j in zip(back_x,back_y):
                if i<0 and i>-0.5 and j <0.5 and j>-0.5:
                    back_obstacle:int = 1
                else:
                    back_obstacle:int = 0

            for i,j in zip(front_x,front_y):
                if i<=1 and j <=0.3 and j>=-0.3:
                    front.append(abs(i))
                else:
                    front.append(1)

            front_dis= min(front)
            
            if len(left_0_1) != 0 and len(left_1_2) != 0 and len(left_2_3) != 0 and len(right_0_1) != 0 and len(right_1_2) != 0 and len(right_2_3) != 0:

                left_0, left_1, left_2 = min(left_0_1), min(left_1_2), min(left_2_3)
                right_0, right_1, right_2 = min(right_0_1), min(right_1_2), min(right_2_3)

                left_index = (2 * left_0 + left_1 + 0.3 * left_2) / (2 + 1 + 0.3)
                right_index = (2 * right_0 + right_1 + 0.3 * right_2) / (2 + 1 + 0.3)


                left_direction = 1 - left_index
                right_direction = 1 - right_index
                
                left_vel = left_direction * 60
                right_vel = right_direction * 60

                if left_vel<10 and right_vel<10:
                    left_vel =left_vel + 10
                    right_vel = right_vel + 10

                elif left_vel>=10 and right_vel<10 and right_vel <= 5:
                    left_vel = left_vel + 5
                    right_vel = 10
                elif left_vel>=10 and right_vel<10 and right_vel > 5:
                    left_vel = left_vel + (10 - right_vel)
                    right_vel = 10

                elif right_vel>=10 and left_vel<10 and left_vel <= 5:
                    left_vel = 10
                    right_vel = right_vel + 5
                elif right_vel>=10 and left_vel<10 and left_vel > 5:
                    left_vel = 10
                    right_vel = right_vel + (10-right_vel)
                    
                elif left_vel<10 and right_vel>=10 :
                    left_vel = 10
                    right_vel = right_vel + (10 - left_vel)
                   
                velocity = f'{int(left_vel)}  {int(right_vel)}  {int(front_dis*100)} {back_obstacle}\r\n'
                left_vel = 0
                right_vel = 0
                left_cnt = 0
                right_cnt = 0

            if data2 != None:
                
                if int(front_dis*100) == 100:
                    print("Go to target")
                    client_socket.send(data2)
                else:
                    print("회피코드 동작",velocity)
                    client_socket.send(velocity.encode())

                    


        ret1 = laser_front.turnOff()
        ret2 = laser_back.turnOff()

    laser_front.disconnecting()
    laser_back.disconnecting()
