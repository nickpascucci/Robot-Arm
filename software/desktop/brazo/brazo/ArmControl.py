"""
    armcontrol.py
    Class definitions for controlling a robot arm through the PyGTK interface.
    Uses pyserial to communicate to the serial port.
"""

import glob
import serial
import time


class ArmControl:
    """
    Control a robot arm over a serial port. 

    This class facilitates message passing through methods which wrap the serial 
    protocol. Generally, this will be talking to a robot arm over a USB-TTY/UART
    connection.
    """
    # Listing of commands recognized by the firmware.
    commands = {"kCOMM_ERROR": "0",
        "kACK": "1",
        "kARDUINO_READY": "2",
        "kERR": "3",
        "kPOSITION": "4",
        "kSPEED": "5",
        "kGRIP": "6",
        "kCOMPLETE": "7",
        "kHOLDER2": "8",
        "kHOLDER3": "9",
        "kHOLDER4": "10",
        "kHOLDER5": "11",
        "kHOLDER6": "12",
        "kHOLDER7": "13",
        "kHOLDER8": "14",
        "kHOLDER9": "15",
        "kHOLDER10": "16",
        "set-position": "17", 
        "set-speed": "18", 
        "set-grip": "19", 
        "toggle-led": "20"}

    def __init__(self, ser_port):
        """
        Initialize the connection using the given port.

        May raise an exception.
        """

        self.__serial = serial.Serial(port=ser_port, timeout=1, writeTimeout=1) # Defaults are OK. 8N1 9600b
        try:
            self.__serial.open()
        except serial.SerialException as e:
            raise Exception("Could not open serial port.")

    def move_base(self, degrees):
        """Rotate the base of the arm by the specified amount."""
        
        
    def move_shoulder(self, degrees):
        """Rotate the shoulder of the arm by the specified amount."""
        
        
    def move_elbow(self, degrees):
        """Rotate the elbow of the arm by the specified amount."""
        
        
    def rotate_wrist(self, degrees):
        """Rotate the wrist of the arm by the specified amount."""
        
    
    def flex_wrist(self, degrees):
        """Flex the wrist of the arm by the specified amount."""
        
        
    def rotate_gripper(self, degrees):
        """Rotate the gripper of the arm by the specified amount."""
        
        
    def open_grip(self):
        """Open the arm's gripper."""
        
        
    def close_grip(self):
        """Close the arm's gripper."""
        
    
    def read_base_angle(self):
        """Read the current base position and return it."""
        
        
    def read_shoulder_angle(self):
        """Read the current base position and return it."""
        
        
    def read_elbow_angle(self):
        """Read the current base position and return it."""
        
        
    def read_wrist_rotation_angle(self):
        """Read the current base position and return it."""
        
        
    def read_wrist_flexion_angle(self):
        """Read the current base position and return it."""
        
        
    def read_gripper_angle(self):
        """Read the current base position and return it."""
        
        
    def read_gripper_closed(self):
        """Read the state of the gripper and return True if closed."""

    def get_current_pose(self):
        base = self.read_base_angle()
        shoulder = self.read_shoulder_angle()
        elbow = self.read_elbow_angle()
        wrist_rot = self.read_wrist_rotation_angle()
        wrist_flex = self.read_wrist_flexion_angle()
        grip_rot = self.read_gripper_angle()
        grip = self.read_gripper_closed()
        pose = Pose(base, shoulder, elbow, wrist_rot, wrist_flex, grip_rot, grip)
        return pose

    def move_to_pose(self, pose):
        """Moves the robot into the given pose."""
        self.move_base(pose.base)
        self.move_shoulder(pose.shoulder)
        self.move_elbow(pose.elbow)
        self.rotate_wrist(pose.wristRot)
        self.flex_wrist(pose.wristFlex)
        self.rotate_grip(pose.gripRot)
        if pose.grip == 0:
            self.close_grip()
        else:
            self.open_grip()
            
    # Writes the command to the serial line in a manner understood by the firmware.
    def send_command(self, command, *args):
	print "Sending command."
	cmd_str = ArmControl.commands[command]
	args_str = ",".join(args)
	if len(args_str) > 0:
            args_str = "," + args_str
        print  "Arguments:", args_str
        msg = cmd_str + args_str + ";"
        print "Message:", msg
        bytes = self.__serial.write(msg)
        print "Bytes:", bytes, "written"
    
    def read_available(self):
        num_avail = self.__serial.inWaiting()
        return self.__serial.read(num_avail)

    def read(self, num):
        return self.__serial.read(num)
            
    def flush(self):
        self.__serial.flushInput()
        self.__serial.flushOutput()
    
    def close_connection(self):
        """Close the serial connection."""
        self.__serial.close()

class Pose:
    """Stores a pose of the arm."""

    def __init__(self, base=0, shoulder=0, elbow=0, wristRot=0, wristFlex=0, gripRot=0, speeds=None, gripClose=False):		
        """Create a new pose with the given angles and speeds.
        
        The angles are specified as independent arguments, speeds are specified as a 6-tuple from 
        base to grip rotation.
        """
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wristRot = wristRot
        self.wristFlex = wristFlex
        self.gripRot = gripRot
        self.gripClose = gripClose
        self.speeds = speeds

    def __str__(self):
        """Print the informal representation of this object as a string."""
        str = "<Base: {0}, Shoulder: {1}, Elbow: {2}, Wrist Rotation: {3}, Wrist Flexion: {4}, Grip Rotation: {5}, Grip Closed: {6}>".format(self.base,
        self.shoulder,
        self.elbow,
        self.wristRot,
        self.wristFlex,
        self.gripRot,
        self.gripClose)
        return str
        
    def _short_string(self):
        """Return a short string representation of this object."""
        
        if self.gripClose == True:
            grip = "Closed"
        else:
            grip = "Open"
        str = "<{0}, {1}, {2}, {3}, {4}, {5}, {6}>".format(self.base,
        self.shoulder,
        self.elbow,
        self.wristRot,
        self.wristFlex,
        self.gripRot,
        grip)
        return str
        
        
def get_available_ports():
    """Enumerate available serial ports and return a list of names."""
    return glob.glob('/dev/ttyUSB*')


if __name__ == "__main__":
    # Test module
    ac = ArmControl("/dev/ttyUSB0")
    print "Checking on Arduino..."
    ac.send_command("kARDUINO_READY")
    time.sleep(1)
    response = ac.read(1)
    if str(response) is ArmControl.commands["kACK"]:
        print "Arduino is ready!"
    else:
        print "Arduino responded with", response, "which is not 'Arduino ready'."
    time.sleep(1)
    print "Toggling led..."
    ac.send_command("toggle-led", "1", "2")
    time.sleep(1)
    ac.close_connection()

