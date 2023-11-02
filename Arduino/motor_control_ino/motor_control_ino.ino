#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver myServo = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 600

//uint8_t SERVOMAX = map(120, 0, 180, 150, 600);

//3 - Head
//8 - shoulder
//9 - shoulder axis
//10 - gripper
//11 - elbow

uint8_t head = 3;
uint8_t base_link = 8;
uint8_t shoulder = 9;
uint8_t gripper = 10;
uint8_t elbow = 11;

uint8_t servonum = 11;
uint8_t numberOfServos = 6;

void setup() {
  Serial.begin(9600);
  myServo.begin();
  myServo.setPWMFreq(60);
  delay(10);
//  wave();
}
// 
void loop() {

  if(Serial.available() > 0){  
  String command = Serial.readString();
//  Serial.println(command.equals(string1));
  
  if (command.toInt() != 0) {
      int angle = command.toInt();
        if (angle >0 && angle < 180){
         
      
      // Limit the angle to a reasonable range, e.g., 0-180 degrees
      angle = constrain(angle, 0, 180);

      // Set the head servo to the specified angle
      int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
      myServo.setPWM(head, 0, pulse);
      delay(15); // You can adjust this delay as needed
      
      Serial.print("Head servo set to angle: ");
      Serial.println(angle);
    }

    else if(angle == 200){
      wave();
    }
      
  }
//  else if (!command.equals("wave")){
//    wave();
//  }
  }

}

void wave(){

  int angle_90 = map(90, 0, 180, SERVOMIN, SERVOMAX);

  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
   myServo.setPWM(base_link,  0, pulselen);
   myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
   delay(10);     
  }


//  wave1
  for (uint16_t pulselen=angle_90; pulselen < SERVOMAX; pulselen++){
   myServo.setPWM(shoulder,  0, pulselen);
   delay(3);     
  }

  for (uint16_t pulselen=SERVOMAX; pulselen > SERVOMIN; pulselen--){
   myServo.setPWM(shoulder,  0, pulselen);
   delay(3);     
  }

  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90; pulselen++){
   myServo.setPWM(shoulder, 0, pulselen);
   delay(3);     
  }
//  wave2
  for (uint16_t pulselen=angle_90; pulselen < SERVOMAX; pulselen++){
   myServo.setPWM(shoulder,  0, pulselen);
   delay(3);     
  }

  for (uint16_t pulselen=SERVOMAX; pulselen > SERVOMIN; pulselen--){
   myServo.setPWM(shoulder,  0, pulselen);
   delay(3);     
  }

  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90; pulselen++){
   myServo.setPWM(shoulder, 0, pulselen);
   delay(3);     
  }

  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90-30; pulselen++){
   myServo.setPWM(base_link,  0, pulselen);
   myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
   delay(10);     
  }
  // Detach the base_link servo
  myServo.setPWM(base_link, 0, 0);
  myServo.setPWM(elbow, 0, 0);

  

//  int angle_120 = map(120, 0, 180, SERVOMIN, SERVOMAX);
  
  
//  myServo.setPWM(elbow,  0, SERVOMAX - angle_120);   
//  for (uint16_t pulselen=angle_90; pulselen < angle_90+40; pulselen++){
//    myServo.setPWM(base_link,  0, pulselen);
//    myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
//    delay(10);     
//  }
  
  
}
