/**
    Multiplexer.h - A library for controlling the 74HC4052 serial multiplexer.
    Created by Nicholas Pascucci, May 2011
*/
#ifndef Multiplexer_h
#define Multiplexer_h

#include "WProgram.h"

class Multiplexer
{
    public:
        Multiplexer(int a, int b);
        int select(int channel, int baud);
        
    private:
        int _a;
        int _b;
        int _chan;
};

#endif
