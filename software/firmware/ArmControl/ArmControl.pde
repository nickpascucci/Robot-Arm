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
const int BAUD_RATE = 19200;

// Serial command and control variables.
char field_separator = ',';
char command_separator = ';';
CmdMessenger cmd = CmdMessenger(Serial, field_separator, command_separator);

// Arduino -> PC messages.

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
  kDIAGNOSTICS = 8,
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
  read_pos,
  
};

void setup(){
  pinMode(13, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(7, LOW);
  
  cmd.print_LF_CR();
  cmd.attach(kARDUINO_READY, arduino_ready);
  cmd.attach(kDIAGNOSTICS, run_diagnostics);
  cmd.attach(unknown_command);
  attach_callbacks(messengerCallbacks);
  
  selectAX12();
  for(int i = 0; i < 3; i++){
    //torque_on(i);
    TorqueOn(i);
  }
  
  selectUSB();
  arduino_ready();
  run_diagnostics();
}

void loop(){
  cmd.feedinSerialData(); // Wait on commands.
}

// CmdMessenger functions

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

void set_position(){
  char arg1[100] = { '\0' };
  char arg2[100] = { '\0' };
  get_base_64_data(arg1, 100);
  get_base_64_data(arg2, 100);
  char servo = arg1[0];
  char pos = arg2[0];
  
  cmd.sendCmd(kCOMPLETE, "Position set");
}

void print_pos_ack(char servo, char pos){
  String acknowledge = "Setting servo " + String(servo, DEC) + " to position " + String(pos, DEC);
  char ack_chars[40] = { '\0' };
  acknowledge.toCharArray(ack_chars, 40);
  cmd.sendCmd(kACK, ack_chars);
}

void set_speed(){
  cmd.sendCmd(kCOMPLETE, "Speed set");
}

void set_grip(){
  cmd.sendCmd(kCOMPLETE, "Grip set");
}

void toggle_led(){
  cmd.sendCmd(kACK, "Blinking!");
  char data[100] = { '\0' };
  get_base_64_data(data, 100);
  char repetitions = data[0];
  for (int i = 0; i < repetitions; i++){
    digitalWrite(13, !digitalRead(13));
    delay(500);
    digitalWrite(13, !digitalRead(13));
    delay(500);
  }
}

void read_pos(){
  char arg1[100] = { '\0' };
  get_base_64_data(arg1, 100);
  char servo = arg1[0];
  
  char pos = query_servo_pos(servo);
  
  char out[10] = { '\0' };
  char args[1] = {servo};
  base64_encode(out, args, 1);
  cmd.sendCmd(kACK, out); // Send ACK and servo position
}

void set_servo_pos(char servo, char pos){
  // Implement AX12 and OpenServo specific handling here.
  if(servo < 3){
    // AX12
    selectAX12();
    SetPosition((int) servo, (int) pos);
    delay(5);
    selectUSB();
    delay(5);
  }
  else{
    // OpenServo
    
  }
}

char query_servo_pos(char servo){
  // Implement AX12 and OpenServo specific handling here.
  if(servo < 3){
    // AX12
    
  }
  else{
    // OpenServo
    
  }
}

// Helper functions

/**
  Selects the AX12 line on the serial multiplexer.
*/
void selectAX12(){
  digitalWrite(7, HIGH);
  Serial.end();
  delay(5);
  mux.select(AX12);
  ax12Init(1000000);
}

/**
  Selects the USB line on the serial multiplexer.
*/
void selectUSB(){
  digitalWrite(7, LOW);
  Serial.end(); //Hopefully this will turn off the AX12 comms.
  delay(5);
  int chan = mux.select(USB);
  if(chan != USB){
    toggle_led();
  }
  Serial.begin(BAUD_RATE);
}

void torque_on(int id){
  ax12SetRegister(id, AX_TORQUE_ENABLE, 1);
}

void get_base_64_data(char *out, int len){
  if(cmd.available())
  {
    // Read data into temporary storage
    char in[350] = { '\0'};
    cmd.copyString(in, 350);
    if(in[0]){
      // Decode into the given buffer.
      int decoded = base64_decode(out, in, len);
    }
  }
}

void run_diagnostics(){
  for(int i=0; i<6; i++){
    set_servo_pos(i, 100);
  }
  delay(1000);
  cmd.sendCmd(kACK, "Done!");
}













