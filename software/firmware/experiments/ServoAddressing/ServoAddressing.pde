/**
  Programs a servo to have the specified address.
**/

#include <ax12.h>
#include <BioloidController.h>

BioloidController bioloid = BioloidController(1000000);

int led = 11;
int led2 = 12;
int button = 10;
int ID = 0;

void setup(){
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
  digitalWrite(9, LOW);
  digitalWrite(8, LOW);
  pinMode(led2, OUTPUT);
  blink(ID);
  
  ax12SetRegister(254, AX_ID, ID); 
  TorqueOn(1);
  ax12SetRegister2(ID, AX_GOAL_SPEED_L, 100);
}

void loop(){
  digitalWrite(led, HIGH);
  delay(500);
  digitalWrite(led, LOW);
  for(int i=0; i<1024; i++){
    ax12SetRegister2(ID, AX_GOAL_POSITION_L, i);
    delay(5);
  }

  digitalWrite(led, HIGH);
  delay(500);
  digitalWrite(led, LOW);
  for(int i=1024; i>0; i--){
    ax12SetRegister2(ID, AX_GOAL_POSITION_L, i);
    delay(5);
  }
}

void waitForInput(){
  pinMode(led, OUTPUT);
  pinMode(button, INPUT);

  
  digitalWrite(led, HIGH);
  while(!digitalRead(button))
  {
    delay(10);
  }
  digitalWrite(led, LOW);
}

void blink(int times){
  for(int i=0; i<times; i++){
    digitalWrite(led2, HIGH);
    delay(500);
    digitalWrite(led2, LOW);
    delay(500);
  }
}
