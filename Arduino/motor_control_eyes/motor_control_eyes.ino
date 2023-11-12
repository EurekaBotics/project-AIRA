#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#define SERVOMIN 150
#define SERVOMAX 600

const byte numChars = 12;
int receivedChars[numChars]; // an array to store the received data

boolean newData = false;

/*
Arduino Pin Connection - Torso
  3 - Head
  8 - shoulder
  9 - shoulder axis
  10 - gripper
  11 - elbow
*/

/*
Arduino Pin Connection - Emotions from Torso to head
  lookright => 2 - 6
  lookleft => 4 - 7
  happy => 5 - 8
  angry => 6 - 10
  sad => 7 - 9
*/

Adafruit_PWMServoDriver myServo = Adafruit_PWMServoDriver();

//Motors
uint8_t lookright = 2;
uint8_t lookleft = 4;
uint8_t happy = 5;
uint8_t angry = 6;
uint8_t sad = 7;

//Emotions
uint8_t head = 3;
uint8_t base_link = 8;
uint8_t shoulder = 9;
uint8_t gripper = 10;
uint8_t elbow = 11;

int t = 2000;

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

}

void loop() {
  
  read();
  process();

}

void read() {

  static byte ndx = 0;
  char endMarker = '\n';
  int command;

  while(Serial.available() > 0 && newData == false) {

      command = Serial.read();

      if (command != endMarker) {
          receivedChars[ndx] = command;
          ndx++;
          if (ndx >= numChars) {
              ndx = numChars - 1;
          }
      }
      else {
          receivedChars[ndx] = '\0';
          ndx = 0;
          newData = true;
      }
  }

}

void process() {

  if (newData == true) {
    digitalWrite(sad, LOW);
    digitalWrite(lookleft, LOW);
    digitalWrite(lookright, LOW);
    digitalWrite(angry, LOW);
    digitalWrite(happy, LOW);
    int angle = 0;

    for (int i = 0; i < numChars && receivedChars[i] != '\0'; i++) {
        angle = angle * 10 + (receivedChars[i] - '0');
    }
    Serial.println(angle);

    if (angle > 0 && angle < 180) {              
        int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
        myServo.setPWM(head, 0, pulse);
        delay(10);
        Serial.print("Head servo set to angle: ");
        Serial.println(angle);
    }
    //Arm motions
    else if(angle == 200){
        hi();
    }
    else if(angle == 201){
        wave();
    }
    else if(angle == 202){
        salute();
    }
    //Emotions
    else if(angle == 300){
        digitalWrite(lookright, HIGH);  
        delay(t);
    }
    else if(angle == 301){
        digitalWrite(lookleft, HIGH);
        delay(t);
    }
    else if(angle == 302){
        digitalWrite(happy, HIGH);
        delay(t);
    }
    else if(angle == 303){
        digitalWrite(sad, HIGH);
        delay(t);
    }
    else if(angle == 304){
        digitalWrite(angry, HIGH);
        delay(t);
    }
    newData = false;
  }
}


void wave() {
    int angle_90 = map(90, 0, 180, SERVOMIN, SERVOMAX);

    for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
        myServo.setPWM(base_link,  0, pulselen);
        myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
        delay(10);     
    }

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
    int salute_angle = SERVOMAX-140;

    for (uint16_t pulselen=angle_90; pulselen > SERVOMIN; pulselen--){
      myServo.setPWM(base_link,  0, pulselen);
      myServo.setPWM(elbow,  0, SERVOMAX - 70 - pulselen);   
      delay(10);     
    }

    for (uint16_t pulselen=angle_90; pulselen < salute_angle; pulselen++){
      myServo.setPWM(shoulder, 0, pulselen);
      delay(3);     
    }
    delay(3000);

    for (uint16_t pulselen = salute_angle; pulselen > angle_90; pulselen--){
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

