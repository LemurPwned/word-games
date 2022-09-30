#include <ezButton.h>

#define DIODE_OUT A0
#define KEY_IN A1
#define RELAY_OUT 5
int key;
int dbCount = 0;
void setup()
{
    // put your setup code here, to run once:
    pinMode(DIODE_OUT, OUTPUT);
    pinMode(KEY_IN, INPUT);
    pinMode(RELAY_OUT, OUTPUT);
    Serial.begin(9600);
}
// poziomo wyłączone

void loop()
{
    // put your main code here, to run repeatedly:
    //  digitalWrite(RELAY_OUT, HIGH);
    key = analogRead(KEY_IN);
    Serial.println(key);
    if (key > 1000)
    {
        dbCount += 1;
        if (dbCount > 100)
        {
            dbCount = 100;
        }
    }
    else
    {
        dbCount = 0;
    }

    if (dbCount > 10)
    {
        analogWrite(DIODE_OUT, 1024);
        digitalWrite(RELAY_OUT, LOW);
    }
    else
    {
        delay(100);
        analogWrite(DIODE_OUT, 0);
        digitalWrite(RELAY_OUT, HIGH);
    }
}
