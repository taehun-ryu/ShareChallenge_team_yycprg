#include <string.h>

byte rx_data[4];
byte rx_buffer[5];

bool rcv_chk = 0;
bool rcv_status = 0;
byte rcv_data = 0;
byte rcv_checksum = '0';
int rcv_index = 0;
int rcv_ready = 0;
int rcv_mode = 0;

int left_vel = 0;
int right_vel = 0;


void setup() {
  Serial.begin(9600);
}

void loop() {


  if (Serial.available()) {
    rcv_data = Serial.read();
    //Serial.println(rcv_data,HEX);
    rcv_chk ^= 1;

    switch (rcv_mode) {

      //initial byte가 걸러지지 않는다...왜? -> checksum성공
      case 0:
        if ((rcv_ready == 0) && (rcv_data == 0xFF)) {
          rcv_mode = 1;
        } else {
          rcv_mode = 0;
        }

      case 1:
        if ((rcv_ready == 0) && (rcv_data == 0xFF)) {
          rcv_mode = 2;
          rcv_ready = 1;
        } else {
          rcv_mode = 0;
        }

      case 2:
        rx_buffer[rcv_index] = rcv_data;
        rcv_index++;

        //checksum 체크
        if (rcv_index > 4) {
          rcv_checksum = 0;
          for (int i = 0; i < 4; i++) {
            rcv_checksum ^= rx_buffer[i];
          }
          rcv_checksum += 1;
          if (rcv_checksum == rx_buffer[rcv_index - 1]) {
            Serial.println("checksum 동일->통신성공");
            memcpy((char)rx_data, (char)rx_buffer, 4);
            rcv_status = 1;
          }
          rcv_mode = 0;
          rcv_index = 0;
          rcv_ready = 0;
        }
        break;
      default:
        rcv_mode = 0;
        rcv_index = 0;
        rcv_ready = 0;
        break;
    }
  }
  if (rcv_status) {
    rcv_status = 0;
    for (int i = 0; i < 4; i+=2) {
      Serial.print(rx_data[i],HEX);
      Serial.print(", ");
      Serial.println(rx_data[i+1],HEX);
    }

    memcpy(&left_vel, &rx_data[0], 2);
    memcpy(&right_vel, &rx_data[2], 2);
    Serial.print(int(left_vel));
    Serial.print(", ");
    Serial.println(int(right_vel));
  }

}
