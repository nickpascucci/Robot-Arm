#include <ax12.h>

/*
  Robot Arm Firmware
  by Nick Pascucci
  
  Interfaces between the arm servos/end manipulator and the driving computer.
*/

//Constants
#define SERIAL_MUX_0 = 3; //Serial multiplexer/demultiplexer select pins
#define SERIAL_MUX_1 = 4; //1: Computer data connection, 2: Dynamixel chain, 3: End Positioner chain, 4: End manipulator
#define STATUS_DATA = 5; //Data connection LED
#define STATUS_ERR = 6; //Error status LED

/*
  Initializes the arm by setting servos to the initial point, and attempts to
  establish a connection to the computer.
*/
void setup(){
  //Set servos to initial points
  
}

/*
  Constantly checks the computer data line for new input and responds.
*/
void loop(){

}
