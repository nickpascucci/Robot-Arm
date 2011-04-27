#include <ax12.h>
#include <BioloidController.h>

BioloidController bio = BioloidController(1000000);

int i;
void setup(){
    i = 0;
}

void loop(){
    // set AX-12 servo with ID=1, to position i, where 0=<i<1024
    SetPosition(1, i);
    i = (i++)%1024;
}
