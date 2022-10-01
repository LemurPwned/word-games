#include <ezButton.h>
#include <ArduinoJson.h>
#include <Arduino.h>
#define DIODE_OUT A0
#define KEY_IN A1
#define RELAY_OUT 5
#define BTN 12

int key;
int dbCount = 0;
int state = 0;
void setup()
{
    // put your setup code here, to run once:
    pinMode(DIODE_OUT, OUTPUT);
    pinMode(KEY_IN, INPUT_PULLUP);
    pinMode(RELAY_OUT, OUTPUT);
    pinMode(BTN, INPUT_PULLUP);
    digitalWrite(RELAY_OUT, HIGH);

    Serial.begin(9600);
    while (!Serial)
        continue;
}
// poziomo wyłączone

void sendInit(int state)
{
    StaticJsonDocument<200> doc;
    doc["init"] = state;
    serializeJson(doc, Serial);
}



void loop()
{
    // put your main code here, to run repeatedly:
    //  digitalWrite(RELAY_OUT, HIGH);
    key = digitalRead(BTN);
    if (!digitalRead(KEY_IN))
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

    if (dbCount > 5)
    {
        analogWrite(DIODE_OUT, 1024);
        if (!state)
          sendInit(1);
        // digitalWrite(RELAY_OUT, LOW);
        state = 1;
    }
    else
    {

        delay(100);
        analogWrite(DIODE_OUT, 0);
        if (state)
          sendInit(0);
        // digitalWrite(RELAY_OUT, HIGH);
        state = 0;
    }
}
