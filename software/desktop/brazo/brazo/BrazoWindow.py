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
logger = logging.getLogger('brazo')

from brazo_lib import Window
from brazo.AboutBrazoDialog import AboutBrazoDialog
from brazo.PreferencesBrazoDialog import PreferencesBrazoDialog
from brazo.armcontrol import Pose, ArmControl
import brazo.inversekinematics

# See brazo_lib.Window.py for more details about how this class works
class BrazoWindow(Window):
    __gtype_name__ = "BrazoWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(BrazoWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutBrazoDialog()
        #self.PreferencesDialog = PreferencesBrazoDialog()

        # Code for other initialization actions should be added here.
        self.poses = []
        self.selected_pose = None
        lengths = self.get_lengths()
        self.ikcalc = brazo.inversekinematics.IKCalculator(lengths)

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
        
        pose = Pose(base, shoulder, elbow, wristRot, wristFlex, gripRot, gripClose)
        index = 0
        if self.selected_pose != None:
            index = self.poses.index(self.selected_pose) + 1
        self.poses.insert(index, pose)
        self.selected_pose = pose
        self.refresh_text_field()
        #self.ui.textview1.get_buffer().insert_at_cursor(pose._short_string() + "\n")
        
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
        #if page_num == 2:
            #print "On teach page."
            # Start updating the positions
        pass
        
    def get_lengths(self):
        """Get the arm segment lengths from settings page and return as a tuple."""
        height = self.ui.height_spinbutton.get_value()
        upper = self.ui.upper_spinbutton.get_value()
        lower = self.ui.lower_spinbutton.get_value()
        wrist = self.ui.wrist_spinbutton.get_value()
        
        return (height, upper, lower, wrist)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

