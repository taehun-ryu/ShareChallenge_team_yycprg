import serial
import time
import struct

#아두이노 연결
ard = serial.Serial(port='/dev/ttyACM0',baudrate=9600)

#TX데이터 byte형으로 가공
left_vel = struct.pack('>h',1000)
right_vel = struct.pack('>h',2000)

# 총 7byte. header 2 byte, data 4byte, checksum 1 byte
tx_data:bytearray = [bytes.fromhex('ff'),bytes.fromhex('ff'),\
                left_vel[0].to_bytes(1,byteorder="little"),\
                left_vel[1].to_bytes(1,byteorder="little"),\
                right_vel[0].to_bytes(1,byteorder="little"),\
                right_vel[1].to_bytes(1,byteorder="little"),\
                0]

a= b'0'

# checksum bit의 인트형
checksum_int=int.from_bytes(a,byteorder="little")

print(left_vel,", ",right_vel)
while True:
    # checksum 계산
    checksum_int=0
    for i in range(2,6):
        #print(tx_data[i])
        #print(int.from_bytes(tx_data[i],byteorder="little"))
        checksum_int^= int.from_bytes(tx_data[i],byteorder="little")
        pass

    checksum_int+=1
    checksum_byte = checksum_int.to_bytes(1,byteorder="big")
    #print("checksum: ",checksum_int,", ",checksum_byte)
    #print("type: ",type(checksum_int),", ",type(checksum_byte))

    # 계산한 checksum LSB에 할당.
    tx_data[6] = checksum_byte

    for i in range(len(tx_data)):
        # 보내기
        ard.write(tx_data[i])
        #print(sys.getsizeof(tx_data[i]))
        #print(tx_data[i])
        time.sleep(0.02)