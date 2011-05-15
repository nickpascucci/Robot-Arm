/**
    Multiplexer.cpp - A library for controlling the 74HC4052 serial multiplexer.
    Created by Nicholas Pascucci, May 2011
*/

#include "WProgram.h"
#include "Multiplexer.h"
/**
    Creates a new multiplexer interface.
    "a" and "b" are the two pins connected to the a and b channels on the multiplexer; remember
    not to use those as GPIO pins!
*/
Multiplexer::Multiplexer(int a, int b){
    _a = a;
    _b = b;
    pinMode(_a, OUTPUT);
    pinMode(_b, OUTPUT);
    
    digitalWrite(_a, LOW);
    digitalWrite(_b, LOW);
    _chan = 0;
}

/**
    Selects the given channel if possible.
    Returns the current channel; if selection fails, returns last channel.
*/
int Multiplexer::select(int channel){
    switch(channel){
        case 0:
            digitalWrite(_a, LOW);
            digitalWrite(_b, LOW);
            return 0;
        case 1:
            digitalWrite(_a, HIGH);
            digitalWrite(_b, LOW);
            return 1;
        case 2:
            digitalWrite(_a, LOW);
            digitalWrite(_b, HIGH);
            return 2;
        case 3:
            digitalWrite(_a, HIGH);
            digitalWrite(_b, HIGH);
            return 3;
        default:
            return _chan;
    }
}


