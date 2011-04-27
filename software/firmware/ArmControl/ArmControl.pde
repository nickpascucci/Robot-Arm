/**
  Arm Control Sketch
  Listens on the serial line for incoming data,
  parses it and drives AX12 servos based on commands
  from the Arm Control desktop app.
  
  Notes:
  Need to add a way to switch between talking to the
  AX12's and the computer. 

*/

#include <ax12.h>

void setup(){
  selectUSB();
  Serial.print("Arm online, waiting for input.");
}

byte packet[100];
void loop(){
  if(Serial.available() > 0){
    byte first = Serial.read();
    if(first == '$'){
      byte data;
      int i = 0;
      while(data != '#'){
        data = Serial.read();
        packet[i++] = data;
      }
      parsePacket();
    }
  }
}


/**
  Parses a packet and performs the requested operations.
*/
void parsePacket(){
  //TODO Add parsing code; then have it select the AX12 and send commands.
}

/**
  Selects the AX12 line on the serial multiplexer.
*/
void selectAX12(){
  Serial.end();
  digitalWrite(9, LOW);
  digitalWrite(8, LOW);
  ax12Init(1000000);
}

/**
  Selects the USB line on the serial multiplexer.
*/
void selectUSB(){
  Serial.end(); //Hopefully this will turn off the UART.
  digitalWrite(9, HIGH);
  digitalWrite(8, LOW);
    Serial.begin(9600);
}
