#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver myServo = Adafruit_PWMServoDriver();

#define SERVOMIN 150
#define SERVOMAX 600

//uint8_t SERVOMAX = map(120, 0, 180, 150, 600);

uint8_t lookright = 2;
uint8_t lookleft = 4;
uint8_t happy = 5;
uint8_t angry = 6;
uint8_t sad = 7;


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

int t = 2000;

uint8_t servonum = 11;
uint8_t numberOfServos = 6;

void setup() {
  Serial.begin(9600);

  pinMode(lookright, OUTPUT);
  pinMode(lookleft, OUTPUT);
  pinMode(happy, OUTPUT);
  pinMode(sad, OUTPUT);
  pinMode(angry, OUTPUT);
  myServo.begin();
  myServo.setPWMFreq(60);
  delay(10);
//  wave();
}

void loop() {

//  Serial.println(Serial.available());
  
  if(Serial.available() > 0)
  {  
//  String command = Serial.readString();
//  Serial.println(command.equals(string1));
  int command = Serial.parseInt();

  digitalWrite(sad, LOW);
    digitalWrite(lookleft, LOW);
    digitalWrite(lookright, LOW);
    digitalWrite(angry, LOW);
    digitalWrite(happy, LOW);
      int angle = command;
      Serial.println(command);
        if (angle >0 && angle < 180){
         
      
      // Limit the angle to a reasonable range, e.g., 0-180 degrees
      angle = constrain(angle, 0, 180);

      // Set the head servo to the specified angle
      int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
      myServo.setPWM(head, 0, pulse);
//      delay(15); // You can adjust this delay as needed
      
      Serial.print("Head servo set to angle: ");
      Serial.println(angle);
    }

    else if(angle == 200){
      // wave();
      salute();
    }

    else if(angle == 300){
      digitalWrite(lookright, HIGH);  
      delay(t);
    }

    else if(angle == 400){
      digitalWrite(lookleft, HIGH);
      delay(t);
    }

    else if(angle == 500){
      digitalWrite(happy, HIGH);
      delay(t);
    }

    else if(angle == 600){
      digitalWrite(sad, HIGH);
      delay(t);
    }

    else if(angle == 700){
      digitalWrite(angry, HIGH);
      delay(t);
    }}}


void wave(){
  int angle_90 = map(90, 0, 180, SERVOMIN, SERVOMAX);
  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
   myServo.setPWM(base_link,  0, pulselen);
   myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
   delay(10);     
  }

// Wave 2 times
for (int var=0; var<2; var++){
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

void hi(){
  int angle_90 = map(90, 0, 180, SERVOMIN, SERVOMAX);
  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
   myServo.setPWM(base_link,  0, pulselen);
   myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
   delay(10);     
  }
  delay(2000);
  for (uint16_t pulselen=SERVOMIN; pulselen < angle_90-30; pulselen++){
   myServo.setPWM(base_link,  0, pulselen);
   myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
   delay(10);     
  }
  // Detach the base_link servo
  myServo.setPWM(base_link, 0, 0);
  myServo.setPWM(elbow, 0, 0);
}


void salute(){
  int angle_90 = map(90, 0, 180, SERVOMIN, SERVOMAX);
  for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
   myServo.setPWM(base_link,  0, pulselen);
   myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
   delay(10);     
  }


  for (uint16_t pulselen=angle_90; pulselen < SERVOMAX-30; pulselen++){
   myServo.setPWM(shoulder, 0, pulselen);
   delay(3);     
  }

  for (uint16_t pulselen=SERVOMAX; pulselen > SERVOMIN-90; pulselen--){
   myServo.setPWM(shoulder,  0, pulselen);
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
}

