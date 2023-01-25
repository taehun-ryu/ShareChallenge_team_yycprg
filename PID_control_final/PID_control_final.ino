#include <TimerFive.h>

//모터 1 관련 설정
#define ENC1_CHA 20  //모터1 엔코더
#define ENC1_CHB 2

#define M1_DIR1 8    //모터1 구동
#define M1_DIR2 12
#define M1_PWM 10

//모터 2 관련설정
#define ENC2_CHA 21  //모터2 엔코더
#define ENC2_CHB 3

#define M2_DIR1 6    //모터2 구동
#define M2_DIR2 7
#define M2_PWM 9

////////////////////타이머 오버플로 확인하기 위한 변수
extern volatile unsigned long timer0_millis;

//PID and FLAG INITIALIZE
double  Kp     = 0.9;
double  Ki     = 0.15;
double  Kd     = 0.025;
char    sec    = NULL;

int     e1cnt  = 0;
int     e2cnt  = 0;

int     e1cnt_k = 0,
        e1cnt_k_1 = 0,
        d_e1cnt = 0;

int     e2cnt_k = 0,
        e2cnt_k_1 = 0,
        d_e2cnt = 0;

double  m1_ref_spd = 0;
double  m1speed = 0;
double  ipwm_u = 0;

double  m2_ref_spd = 0;
double  m2speed = 0;
double  ipwm2_u = 0;

bool    t5_flag = 0;

//odometric calculation을 위한 변수
float L = 60;
float R = 20;

float initAngle = 0;
int x = 0;
float dltTheta = 0;
float dltDistance = 0;

float tmp_l;
float tmp_r;

float dltDistL = 0;
float dltDistR = 0;

float now_x = 0;
float now_y = 0;
float now_theta = 0;

//magnetic algorithm(numb)
int target_x = 144;
int target_y = -104;
float target_theta = 0.;

//PID value holder
float m1_err_spd = 0;
float m1_err_spd_k_1 = 0;
float m1_derr_spd = 0;
float m1_err_sum = 0;

float ctrl_up = 0;
float ctrl_ui = 0;
float ctrl_ud = 0;
int ctrl_u = 0;

float m2_err_spd = 0;
float m2_err_spd_k_1 = 0;
float m2_derr_spd = 0;
float m2_err_sum = 0;

float ctrl2_up = 0;
float ctrl2_ui = 0;
float ctrl2_ud = 0;
int ctrl2_u = 0;

int Rccnt = 0, Rfcnt = 0;
int Lccnt = 0, Lfcnt = 0;

float m_spd = 0;
//for serialEvent function
bool u2_rcv_flag = false;
byte u2_rcv_data = '0';
//motorpart ends
int joy_x = 507;
int joy_y = 504;
bool in_key[7];


//for UART2
bool rcv_chk = 0;
bool rcv_status = 0;
bool rcv_ready = 0;
byte rcv_data = 0;
byte rcv_checksum = 0;
byte rx_buffer[5];
byte rx_data[5];
int rcv_count = 0;
int rcv_index = 0;

//////////////////init angle
int degree = 0;
int Lled = 24;
int Mled = 25;
int Rled = 26;
int tact = 27;
int tactcon = 0;
int steps;
int initial_angle;
void setup() {
  pinMode(ENC1_CHA, INPUT_PULLUP);
  pinMode(ENC1_CHB, INPUT_PULLUP);
  pinMode(M1_DIR1, OUTPUT);
  pinMode(M1_DIR2, OUTPUT);
  pinMode(M1_PWM, OUTPUT);
  pinMode(ENC2_CHA, INPUT_PULLUP);
  pinMode(ENC2_CHB, INPUT_PULLUP);
  pinMode(M2_DIR1, OUTPUT);
  pinMode(M2_DIR2, OUTPUT);
  pinMode(M2_PWM, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(ENC1_CHA), Enc1chA_ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC1_CHB), Enc1chB_ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC2_CHA), Enc2chA_ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC2_CHB), Enc2chB_ISR, CHANGE);
  digitalWrite(M1_DIR1, LOW);
  digitalWrite(M1_DIR2, HIGH);
  analogWrite(M1_PWM, 0);
  digitalWrite(M2_DIR1, LOW);
  digitalWrite(M2_DIR2, HIGH);
  analogWrite(M2_PWM, 0);
  Serial.begin(115200);
  Serial.setTimeout(50);
  Timer5.initialize(50000); //50msec,
  Timer5.attachInterrupt(T5ISR); //T5ISR

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  if (Serial.available() > 0) {
    sec = (char)Serial.read();
    //m1은 대문자
    if (sec == 'S') {                // wait for a second
      digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW

      m1_ref_spd = Serial.parseFloat();
    }
    // m2는 소문자
    else if (sec == 's') {

      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      m2_ref_spd = Serial.parseFloat();

    }
    else if (sec == 'n') {

      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      now_x = Serial.parseFloat();

    }
  }
    Serial.print("s:  ");
    Serial.print(m2_ref_spd);
    Serial.print("     S:  ");
    Serial.print(m1_ref_spd);
    Serial.print("     nowx:  "); 
    Serial.print(now_x);
    Serial.print("     nowy:  ");
    Serial.print(now_y);
    Serial.print("     now_theta:  ");
    Serial.println(now_theta * 180 / 3.14);
    ComputePID();
  

  Kp     = 0.9;
  Ki     = 0.15;
  Kd     = 0.025;
  sec = NULL;
  ComputePID();
}

////////////////////////////////////odometric calculation//////////////////////////////////////

//len 이동할 거리, mil 이동할 시간, x 기준시간, a 완속 구간비율
float calcMove(int len, int mil, int x , float a) {
  float RPM = (60 * len) / (6.7 * 3.141592 * mil) * 1000;
  float RPM_last = RPM / (1 - a);
  float RPM_Tri = 0;
  if (millis() - x < mil * a) {
    RPM_Tri = RPM_last * ((millis() - x) / (mil * a));
  } else if (mil * a <= (millis() - x) && (millis() - x) < (mil - mil * a)) {
    RPM_Tri = RPM_last;
  } else {
    RPM_Tri = RPM_last - RPM_last * (((millis() - x) - (mil - mil * a)) / (mil * a));
  }
  //Serial.println("calcMove");
  return RPM_Tri;
}

//len 회전할 각도(deg), mil 이동할 시간, x 기준시간, a 완속 구간비율
float calcTheta(int theta, int mil, int x , float a) {
  float RPM = (17.25 * theta * (3.141592 / 360) * 60) / (6.7 * 3.141592 * mil) * 1000;
  float RPM_last = RPM / (1 - a);
  float RPM_Tri = 0;
  if (millis() - x < mil * a) {
    RPM_Tri = RPM_last * ((millis() - x) / (mil * a));
  } else if (mil * a <= (millis() - x) && (millis() - x) < (mil - mil * a)) {
    RPM_Tri = RPM_last;
  } else {
    RPM_Tri = RPM_last - RPM_last * (((millis() - x) - (mil - mil * a)) / (mil * a));
  }
  //Serial.println("calcTheta");
  return RPM_Tri;
}

void ComputePID() {
  /*
    PID CALCULATION

    pid bidirectional calculation for Motor control for Mobile robot
    Calculate both motors value simultaniously.
    Didn't consider the timing adjust or mode change
    So It can only usable as motor controller

  */
  //Error
  if (t5_flag) {
    t5_flag = 0;

    m1speed = -(d_e1cnt * 10 / 11);            // *500/11/50
    m2speed = -(d_e2cnt * 10 / 11);            // *500/11/50


    //Error
    m1_err_spd = m1_ref_spd - m1speed;
    m1_derr_spd = m1_err_spd - m1_err_spd_k_1;
    m1_err_sum = m1_err_sum + m1_err_spd;
    m1_err_spd_k_1 = m1_err_spd;

    m2_err_spd = m2_ref_spd - m2speed;
    m2_derr_spd = m2_err_spd - m2_err_spd_k_1;
    m2_err_sum = m2_err_sum + m2_err_spd;
    m2_err_spd_k_1 = m2_err_spd;

    //PID-Controller
    ctrl_up = Kp * m1_err_spd;
    ctrl_ui = Ki * m1_err_sum;
    ctrl_ud = Kd * m1_derr_spd;

    //PID-Controller
    ctrl2_up = Kp * m2_err_spd;
    ctrl2_ui = Ki * m2_err_sum;
    ctrl2_ud = Kd * m2_derr_spd;

    ctrl_u = (int)(ctrl_up + ctrl_ud + ctrl_ui);
    ctrl2_u = (int)(ctrl2_up + ctrl2_ud + ctrl2_ui);

    if (ctrl_u >= 0) {
      digitalWrite(M1_DIR1, LOW);
      digitalWrite(M1_DIR2, HIGH); //ccw
      if (ctrl_u > 255) ipwm_u = 255;
      else ipwm_u = (int)ctrl_u;
    }
    else {
      digitalWrite(M1_DIR1, HIGH);
      digitalWrite(M1_DIR2, LOW); //cw
      if (ctrl_u < -255) ipwm_u = 255;
      else ipwm_u = (int)ctrl_u * (-1);
    }

    if (ctrl2_u >= 0) {
      digitalWrite(M2_DIR1, LOW);
      digitalWrite(M2_DIR2, HIGH); //ccw
      if (ctrl2_u > 255) ipwm2_u = 255;
      else ipwm2_u = (int)ctrl2_u;
    }
    else {
      digitalWrite(M2_DIR1, HIGH);
      digitalWrite(M2_DIR2, LOW); //cw
      if (ctrl2_u < -255) ipwm2_u = 255;
      else ipwm2_u = (int)ctrl2_u * (-1);
    }

    analogWrite(M1_PWM, ipwm_u);
    analogWrite(M2_PWM, ipwm2_u);
  }
}
void T5ISR() {
  t5_flag = 1;

  e1cnt_k = e1cnt;
  d_e1cnt = e1cnt_k - e1cnt_k_1; //delta_error
  e1cnt_k_1 = e1cnt_k;

  e2cnt_k = e2cnt;
  d_e2cnt = e2cnt_k - e2cnt_k_1; //delta_error
  e2cnt_k_1 = e2cnt_k;
  odometry();
}

//m1 엔코더 계산
void Enc1chA_ISR() {
  if (digitalRead(ENC1_CHA) == HIGH) {
    if (digitalRead(ENC1_CHB) == LOW) e1cnt--;
    else e1cnt++;
  }
  else {
    if (digitalRead(ENC1_CHB) == HIGH) e1cnt--;
    else e1cnt++;
  }
}

void Enc1chB_ISR() {
  if (digitalRead(ENC1_CHB) == HIGH) {
    if (digitalRead(ENC1_CHA) == HIGH) e1cnt--;
    else e1cnt++;
  }
  else {
    if (digitalRead(ENC1_CHA) == LOW) e1cnt--;
    else e1cnt++;
  }
}

// m2 엔코더 계산
void Enc2chA_ISR() {
  digitalWrite(13, LOW);
  if (digitalRead(ENC2_CHA) == HIGH) {
    if (digitalRead(ENC2_CHB) == LOW) e2cnt--;
    else e2cnt++;
  }
  else {
    if (digitalRead(ENC2_CHB) == HIGH) e2cnt--;
    else e2cnt++;
  }
}

void Enc2chB_ISR() {
  digitalWrite(13, LOW);
  if (digitalRead(ENC2_CHB) == HIGH) {
    if (digitalRead(ENC2_CHA) == HIGH) e2cnt--;
    else e2cnt++;
  }
  else {
    if (digitalRead(ENC2_CHA) == LOW) e2cnt--;
    else e2cnt++;
  }
}
