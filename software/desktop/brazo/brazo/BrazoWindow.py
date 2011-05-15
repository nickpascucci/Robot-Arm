# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('brazo')

import gtk
import webbrowser
import logging
import time
logger = logging.getLogger('brazo')

from brazo_lib import Window
from brazo.AboutBrazoDialog import AboutBrazoDialog
from brazo.PreferencesBrazoDialog import PreferencesBrazoDialog
from brazo.ArmControl import Pose, ArmControl
import brazo.InverseKinematics

# See brazo_lib.Window.py for more details about how this class works
class BrazoWindow(Window):
    __gtype_name__ = "BrazoWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(BrazoWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutBrazoDialog()
        self.PreferencesDialog = PreferencesBrazoDialog()

        # Code for other initialization actions should be added here.
        self.poses = []
        self.selected_pose = None
        lengths = self.get_lengths()
        self.ikcalc = brazo.InverseKinematics.IKCalculator(lengths)
        
        # Initialize combo box
        liststore = gtk.ListStore(str)
        self.ui.port_combo_box.set_model(liststore)
        cell = gtk.CellRendererText()
        self.ui.port_combo_box.pack_start(cell, True)
        self.ui.port_combo_box.add_attribute(cell, 'text', 0)        
        
        self.armcon = None
        self.enumerate_ports()
        

    def about(self, builder):
        response = self.AboutDialog.run()
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
            self.AboutDialog.hide()
         
         
    def help(self, widget):
        webbrowser.open_new("http://kestrelrobotics.com/support/51-brazo-support/68-brazo-help")
    
    
    def quit(self, builder):
        exit(0)


    def on_torque_toggled(self, widget, data=None):
        
        if widget.get_active():
            widget.set_label("Torque: ON")
        else:
            widget.set_label("Torque: OFF")


    def on_gripper_close_button_toggled(self, widget, data=None):
        if widget.get_active():
            widget.set_label("Closed")
        else:
            widget.set_label("Open")
        
        
    def refresh_text_field(self):
        """Refresh the text field, placing arrows at the selected pose."""
        buffer = self.ui.textview1.get_buffer()
        #Clear the field.
        buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())
        #Add each pose
        for pose in self.poses:
            buffer.insert_at_cursor(pose._short_string())
            if pose == self.selected_pose:
                buffer.insert_at_cursor("  <--")
            buffer.insert_at_cursor("\n")
        
        
    def on_add_pose_button_clicked(self, widget, data=None):
        """Add the input data into a pose and enqueue it."""
        base = self.ui.base_spinner.get_value()
        shoulder = self.ui.shoulder_spinner.get_value()
        elbow = self.ui.elbow_spinner.get_value()
        wristRot = self.ui.wrist_rotation_spinner.get_value()
        wristFlex = self.ui.wrist_flexion_spinner.get_value()
        gripRot = self.ui.gripper_rotation_spinner.get_value()
        gripClose = self.ui.gripper_close_button.get_active()
        speeds = (self.ui.base_speed.get_value(),
        self.ui.shoulder_speed.get_value(),
        self.ui.elbow_speed.get_value(),
        self.ui.wrist_rot_speed.get_value(),
        self.ui.wrist_flex_speed.get_value(),
        self.ui.grip_rot_speed.get_value())
        pose = Pose(base, shoulder, elbow, wristRot, wristFlex, gripRot, speeds, gripClose)
        index = 0
        if self.selected_pose != None:
            index = self.poses.index(self.selected_pose) + 1
        self.poses.insert(index, pose)
        self.selected_pose = pose
        self.refresh_text_field()
        
        
    def on_remove_pose_button_clicked(self, widget, data=None):
        """Remove the selected pose."""
        if len(self.poses) <= 0:
            return
        index = self.poses.index(self.selected_pose)
        self.poses.pop(index)
        if(index > 0):
            self.selected_pose = self.poses[index-1]
        elif len(self.poses) > 0:
            self.selected_pose = self.poses[0]
        else:
            self.selected_pose = None
        self.refresh_text_field()
        
        
    def on_clear_pose_button_clicked(self, widget, data=None):
        """Clear the user input fields."""
        self.ui.base_spinner.set_value(0)
        self.ui.shoulder_spinner.set_value(0)
        self.ui.elbow_spinner.set_value(0)
        self.ui.wrist_rotation_spinner.set_value(0)
        self.ui.wrist_flexion_spinner.set_value(0)
        self.ui.gripper_rotation_spinner.set_value(0)
        self.ui.gripper_close_button.set_active(False)
        
        
    def on_next_button_clicked(self, widget, data=None):
        """Select the next pose."""
        if len(self.poses) <= 0:
            return
        index = self.poses.index(self.selected_pose)
        if(index != len(self.poses)-1):
            self.selected_pose = self.poses[index+1]
        self.refresh_text_field()
    
    
    def on_previous_button_clicked(self, widget, data=None):
        """Select the previous pose."""
        if len(self.poses) <= 0:
            return
        index = self.poses.index(self.selected_pose)
        if(index != 0):
            self.selected_pose = self.poses[index-1]
        self.refresh_text_field()
        
        
    def on_play_button_clicked(self, widget, data=None):
        """Play through the poses."""
        print "Play button clicked."
        for pose in self.poses:
            print pose
        
        
    def on_grab_button_clicked(self, widget, data=None):
        """Grab the arm's current pose and add it to the list."""
        print "Grab position button clicked."
        
        
    def on_calculate_button_clicked(self, widget, data=None):
        x = self.ui.x_spinbutton.get_value()
        y = self.ui.y_spinbutton.get_value()
        z = self.ui.z_spinbutton.get_value()
        try:
            pose = self.ikcalc.get_pose_for_coordinates(x, y, z)
            print "Pose:", pose
        except brazo.inversekinematics.UnreachableError:
            print "Point unreachable."


    def on_save_button_clicked(self, widget, data=None):
        self.ikcalc = brazo.inversekinematics.IKCalculator(self.get_lengths())
        print "Created new ikcalc."
        self.ui.status_label.set_text("Settings committed!")
        
        
    def on_discard_button_clicked(self, widget, data=None):
        pass


    def on_notebook1_switch_page(self, widget, page, page_num, data=None):
        if page_num == 3:
            self.enumerate_ports()
        
        
    def get_lengths(self):
        """Get the arm segment lengths from settings page and return as a tuple."""
        height = self.ui.height_spinbutton.get_value()
        upper = self.ui.upper_spinbutton.get_value()
        lower = self.ui.lower_spinbutton.get_value()
        wrist = self.ui.wrist_spinbutton.get_value()
        return (height, upper, lower, wrist)
        
        
    def on_test_button_clicked(self, widget, data=None):
        if self.armcon is not None:
            self.test_connection()
        else:
            self.set_status("No port selected.", 0.0)
        
        
    def on_diagnostics_button_clicked(self, widget, data=None):
        if self.armcon is not None:
            self.test_connection()
            self.run_diagnostics()
        else:
            self.set_status("Not connected.", 0.0)
        
    def enumerate_ports(self):
        avail_ports = brazo.ArmControl.get_available_ports()
        liststore = self.ui.port_combo_box.get_model()
        liststore.clear()
            
        for i in range(len(avail_ports)):
            port = avail_ports[i]
            liststore.append([port])
            if self.armcon is not None and self.armcon.port == port:
                self.ui.port_combo_box.set_active(i)
        
        if len(avail_ports) == 0:
            self.ui.status_label.set_text("No serial ports found!")
        
        
    def on_port_combo_box_changed(self, widget, data=None):
        # Create new arm control object based on serial port selection
        active_port = self.ui.port_combo_box.get_active()
        if active_port != -1:
            active_port = self.ui.port_combo_box.get_model()[active_port][0]
            self.armcon = ArmControl(active_port)
        
        
    def test_connection(self):
        self.set_status("Testing...", 0.1)
        self.armcon.send_command("kARDUINO_READY")
        
        print "Sent ping"
        response = self.armcon.read(1)
        print "Response:", response
        self.set_status(progress=0.3)
        print "Read response."
        if str(response) is ArmControl.commands["kACK"]:
            self.set_status("Arduino online!", 0.6)
            self.armcon.send_command("toggle-led")
            self.set_status("Success!", 1.0)
        else:
            self.set_status("Connection failed!", 1.0)
            
        self.armcon.flush()
        
    def run_diagnostics(self):
        self.set_status("Connecting...", 0.1)
        self.armcon.send_command("kDIAGNOSTICS")
        time.sleep(.01)
        response = self.armcon.read(1);
        self.armcon.flush()
        print response
        self.set_status("Response: " + response, 0.2)
        print "done."
	
    def set_status(self, text=None, progress=None):
        if text is not None:
            self.ui.status_label.set_text(text)
        if progress is not None:
            self.ui.progressbar.set_fraction(progress)
        
    def finalize(self):
        if self.armcon is not None:
            self.armcon.close()
        
        
        
        
        
        
        

