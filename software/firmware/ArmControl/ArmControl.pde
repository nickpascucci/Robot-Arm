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
#include <Streaming.h>
#include <Base64.h>
#include <CmdMessenger.h>
#include <Multiplexer.h>

// Multiplexer and serial control variables.
Multiplexer mux(8, 9);
const int AX12 = 0;
const int USB = 1;

// Serial command and control variables.
char field_separator = ',';
char command_separator = ';';
CmdMessenger cmd = CmdMessenger(Serial, field_separator, command_separator);

// This enum holds Arduino -> PC messages.
enum {
  // General meta messages
  kCOMM_ERROR = 0,
  kACK = 1,
  kARDUINO_READY = 2,
  kERR = 3,
  
  // Application specific messages. These are specified with octal digits.
  kPOSITION = 4,
  kSPEED = 5,
  kGRIP = 6,
  kCOMPLETE = 7,
  kHOLDER2 = 8,
  kHOLDER3 = 9,
  kHOLDER4 = 10,
  kHOLDER5 = 11,
  kHOLDER6 = 12,
  kHOLDER7 = 13,
  kHOLDER8 = 14,
  kHOLDER9 = 15,
  kHOLDER10 = 16,
  
  kSEND_CMDS_END, // Mid way through our range
  
};

// PC -> Arduino messages
messengerCallbackFunction messengerCallbacks[] = {
  set_position, // 17
  set_speed,
  set_grip,
  toggle_led,
};

void setup(){
  pinMode(13, OUTPUT);
  
  cmd.print_LF_CR();
  cmd.attach(kARDUINO_READY, arduino_ready);
  cmd.attach(unknown_command);
  attach_callbacks(messengerCallbacks);
  
  selectAX12();
  torque_on(1);
  
  selectUSB();
  arduino_ready();

}

void attach_callbacks(messengerCallbackFunction* callbacks){
  int i = 0;
  int offset = kSEND_CMDS_END;
  while(callbacks[i]){
    cmd.attach(offset+i, callbacks[i]);
    i++;
  }
}

void unknown_command(){
  cmd.sendCmd(kERR, "Unknown Command");
}

void arduino_ready(){
  cmd.sendCmd(kACK, "Arduino ready");
}

void loop(){
  // Wait on commands.
  cmd.feedinSerialData();
}

void set_position(){
  cmd.sendCmd(kCOMPLETE, "Position set");
}

void set_speed(){
  cmd.sendCmd(kCOMPLETE, "Speed set");
}

void set_grip(){
  cmd.sendCmd(kCOMPLETE, "Grip set");
}

void toggle_led(){
  digitalWrite(13, !digitalRead(13));
}

// Helper functions

/**
  Selects the AX12 line on the serial multiplexer.
*/
void selectAX12(){
  Serial.end();
  delay(5);
  mux.select(AX12);
  ax12Init(1000000);
}

/**
  Selects the USB line on the serial multiplexer.
*/
void selectUSB(){
  Serial.end(); //Hopefully this will turn off the UART.
  delay(5);
  mux.select(USB);
  Serial.begin(9600);
}

void torque_on(int id){
  ax12SetRegister(id, AX_TORQUE_ENABLE, 1);
}


