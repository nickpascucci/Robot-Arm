#! /usr/bin/python
# Provides an implementation of a fast inverse kinematics calculator. 
# Works for 6DOF arms similar to the Brazo arm.
# Based on the source code from the Kestrel Robotics whitepaper,
# available at http://kestrelrobotics.com/create/white-papers/66-inverse-kinematics

import math

from armcontrol import Pose

class UnreachableError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

class IKCalculator:
    """The IKCalculator class provides inverse kinematics calculations
    for 6DOF arms similar to the Brazo arm. The calculations use a 3D
    Cartesian system, with the origin at the center of the shoulder joint."""

    def __init__(self, lengths):
        """Initialize the calculator using the given arm segment lengths.
        
        The 'lengths' parameter should be a 4-tuple with each of the arm
        segment lengths from axis of rotation to axis, in order from base
        to grip."""
        self.lengths = lengths

    def get_pose_for_coordinates(self, x, y, z):
        """Generate a pose based on the given coordinates.
        
        The returned pose will have the gripper set to false; be sure to
        override this if needed."""
        
        # For now, this does a simplified version of the calculations with
        # no accomodation for taking advantage of the additional 3DOF on the
        # end manipulator.
        # TODO Extend this to take advantage of all degrees of freedom.
        lengths = self.lengths
        k = lengths[0] # From base to shoulder
        l = lengths[1] # From shoulder to elbow
        m = lengths[2] # From elbow to wrist
        n = lengths[3] # From wrist to gripper
        
        #Sanity check. If the point is out of reach of our arm, we should complain.
        distance = math.sqrt(x**2 + y**2 + z**2)
        if distance > l + m + n:
            raise UnreachableError("Point out of range.")
        
        # All of these angles are in radians.
        try:
            delta = math.atan(y/x) # Rotation about the z axis puts arm into abstract plane.
        except ZeroDivisionError:
            delta = 0
        wrist_rotation = 0 # No rotation in the wrist keeps it simple for now
        wrist_flexion = 90 # Keep the wrist straight
        grip_rotation = 0
        
        n_1 = math.sqrt(x**2 + y**2) # Length of x,y projection of the arm.
        x_2 = n_1 # In the abstract plane, our x coordinate is the same as the length above.
        y_2 = z # Abstract plane y coordinate is equal to 3D space z coordinate.
        n_2 = math.sqrt(x_2**2 + y_2**2) # Length of triangle side in abstract plane.
        
        print "Values: n_1 = {0} x_2 = {1} y_2 = {2} n_2 = {3} l = {4} m = {5}".format(n_1, x_2, y_2, n_2, l, m)
        # Angle calculations in the abstract plane.
        print ((l**2 + n_2**2) - m**2)/(2*l*n_2)
        alpha = math.acos((l**2 + n_2**2 - m**2)/(2*l*n_2)) # Shoulder rotation
        beta = math.acos((m**2 + l**2 - n_2**2)/(2*m*l)) # Elbow rotation
        gamma = (math.pi/2) - (alpha - beta)
        nu = math.atan(y_2/x_2) # Angular difference from x,y plane in 3D space
        
        delta = math.degrees(delta)
        alpha = math.degrees(alpha)
        beta = math.degrees(beta)
        gamma = math.degrees(gamma)
        
        pose = Pose(delta, alpha, beta, wrist_rotation, wrist_flexion, grip_rotation)
        return pose
        

