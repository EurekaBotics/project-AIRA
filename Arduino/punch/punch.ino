#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver myServo = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 600

uint8_t head = 3;
uint8_t base_link = 8;
uint8_t shoulder = 9;
uint8_t gripper = 10;
uint8_t elbow = 11;

void setup() {
  
  Serial.begin(115200);
  myServo.begin();
  myServo.setPWMFreq(60);
  delay(10);

}

void loop() {
  
  punch();

}

void punch(){

  int angle_90 = map(90, 0, 180, SERVOMIN, SERVOMAX);
  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--) {
    myServo.setPWM(base_link,  0, pulselen);
    delay(10);     
  }

  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
    myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
    delay(10);     
  }

  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90-30; pulselen++){
    myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
    delay(10);     
  }

  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
    myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
    delay(10);     
  }

  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90-30; pulselen++){
    myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
    delay(10);     
  }

  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90-30; pulselen++){
    myServo.setPWM(base_link,  0, pulselen);
    myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
    delay(10);     
  }

  // Detach the base_link servo
  myServo.setPWM(base_link, 0, 0);
  myServo.setPWM(elbow, 0, 0);

}