#include "HCPCA9685.h"
#include <SoftwareSerial.h> // SoftwareSerial 라이브러리를 사용합니다.
#define I2CAdd 0x40

SoftwareSerial BT(9,8);
HCPCA9685 HCPCA9685(I2CAdd);


void setup() {
  HCPCA9685.Init(SERVO_MODE);
  HCPCA9685.Sleep(false);
  BT.begin(9600);
  Serial.begin(9600);
}

int Pos1 ; // 거리 조절 모터의 현재 상태
int prevPos1 = 210; // 거리 조절 모터의 이전 상태
int Pos2 ; // 높이 조절 모터의 현재 상태
int prevPos2 = 210; // 높이 조절 모터의 이전 상태
int tt = 420; // 모터 가동 범위의 최대 값

void loop() {  
  if (Serial.available() > 0) {
    char input = Serial.read();
    Serial.println(input);
    
    if (input == 'a') { 
      Pos1 = prevPos1 + 42;
      HCPCA9685.Servo(4, Pos1);
      HCPCA9685.Servo(5, tt - Pos1);
      Serial.println(Pos1);
      Serial.println(tt-Pos1);
      prevPos1 = Pos1;
      if(prevPos1 > 470){
        prevPos1 = 420;
      }else if(prevPos1 < 0){
        prevPos1 = 0;
      }
    }
    else if (input == 'b') {
      Pos1 = prevPos1- 42;
      HCPCA9685.Servo(4, Pos1);
      HCPCA9685.Servo(5, tt - Pos1);
      Serial.println(Pos1);
      Serial.println(tt-Pos1);
      prevPos1 = Pos1;
      if(prevPos1 > 470){
        prevPos1 = 420;
      }else if(prevPos1 < 0){
        prevPos1 = 0;
      }
    }
    else if (input == 'c') {
      Pos2 = prevPos2 + 42;
      HCPCA9685.Servo(8, Pos2);
      HCPCA9685.Servo(9, tt - Pos2);
      prevPos2 = Pos2;
      Serial.println(Pos2);
      Serial.println(tt-Pos2);
      if(prevPos2 > 470){
        prevPos2 = 420;
      }else if(prevPos2 < 0){
        prevPos2 = 0;
      }
    }
    else if (input == 'd') {
      Pos2 = prevPos2 - 42;
      HCPCA9685.Servo(8, Pos2);
      HCPCA9685.Servo(9, tt - Pos2);
      Serial.println(Pos2);
      Serial.println(tt-Pos2);
      prevPos2 = Pos2;
      if(prevPos2 > 470){
        prevPos2 = 420;
      }else if(prevPos2 < 0){
        prevPos2 = 0;
      }
    }
  }
}
