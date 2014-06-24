/**
  Runs diagnostic tests on AX12 servos.
**/

#include <ax12.h>

int ONBOARD_LED = 13;
int SER_MUX_A = 8; //S0 on datasheet
int SER_MUX_B = 9; //S1 on datasheet

void setup(){
  delay(1000);
  pinMode(SER_MUX_A, OUTPUT);
  pinMode(SER_MUX_B, OUTPUT);
  enable_usb_serial();
  Serial.begin(9600);
}

void loop(){
  Serial.println("Hi there!");
  delay(500);
}

/*
  Turns on serial communications to the AX12 lines.
*/
void enable_usb_serial(){
  digitalWrite(SER_MUX_A, LOW);
  digitalWrite(SER_MUX_B, HIGH);
}


/*
  Blinks the on board LED.
*/
void blink(int times){
  for(int i=0; i<times; i++){
    digitalWrite(ONBOARD_LED, HIGH);
    delay(500);
    digitalWrite(ONBOARD_LED, LOW);
    delay(500);
  }
}
