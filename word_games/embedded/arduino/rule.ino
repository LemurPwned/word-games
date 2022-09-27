#include <ArduinoJson.h>

#include <TM1637Display.h>
#include <Arduino.h>

#define CLK 2
#define DIO_A 3
#define DIO_B 4
#define DIO_C 5

#define BTN_A 6
#define BTN_B 7
#define BTN_C 8

#define VCC 5.0
#define RESOLUTION 1024.0

const uint8_t SEG_DONE[] = {
    SEG_B | SEG_C | SEG_D | SEG_E | SEG_G,         // d
    SEG_A | SEG_B | SEG_C | SEG_D | SEG_E | SEG_F, // O
    SEG_C | SEG_E | SEG_G,                         // n
    SEG_A | SEG_D | SEG_E | SEG_F | SEG_G          // E
};

bool win = false;
int numberA = 0;
int numberB = 0;
int numberC = 0;
int score = 0;

int btnStateA = 0;
int btnStateB = 0;
int btnStateC = 0;

TM1637Display displayA(CLK, DIO_A);
TM1637Display displayB(CLK, DIO_B);
TM1637Display displayC(CLK, DIO_C);

void setup()
{
    uint8_t data[] = {0xff, 0xff, 0xff, 0xff};
    displayA.setBrightness(0x0f);
    displayB.setBrightness(0x0f);
    displayC.setBrightness(0x0f);
    displayA.setSegments(data);
    displayB.setSegments(data);
    displayC.setSegments(data);

    pinMode(BTN_A, INPUT);
    pinMode(BTN_B, INPUT);
    pinMode(BTN_C, INPUT);

    Serial.begin(9600);
    while (!Serial)
        continue;
}

void displayNumber(int number, TM1637Display display)
{
    // leading zero is set to false
    display.showNumberDec(number, false);
}

void readJson(StaticJsonDocument<200> doc)
{
    win = doc["win"];
    numberA = doc["numbers"][0];
    numberB = doc["numbers"][1];
    numberC = doc["numbers"][2];
    score = doc["score"];

    displayNumber(numberA, displayA);
    displayNumber(numberB, displayB);
    displayNumber(numberC, displayC);
}

void readButtonPress()
{
    btnStateA = digitalRead(BTN_A);
    btnStateB = digitalRead(BTN_B);
    btnStateC = digitalRead(BTN_C);
    while (
        btnStateA == HIGH &&
        btnStateB == HIGH &&
        btnStateC == HIGH)
    {
        btnStateA = digitalRead(BTN_A);
        btnStateB = digitalRead(BTN_B);
        btnStateC = digitalRead(BTN_C);
    }
}

void sendAnswer(int btnStateA, int btnStateB, int btnStateC)
{
    StaticJsonDocument<200> doc;
    if (btnStateA == LOW)
    {
        doc["answer"] = numberA;
    }
    else if (btnStateB == LOW)
    {
        doc["answer"] = numberB;
    }
    else if (btnStateC == LOW)
    {
        doc["answer"] = numberC;
    }
    serializeJsonPretty(doc, Serial);
}

void loop()
{
    while (true)
    {
        if (Serial.available() > 0)
        {
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, Serial);
            if (error)
            {
                Serial.print(F("deserializeJson() failed: "));
                Serial.println(error.c_str());
                return;
            }
            readJson(doc);
            if (win)
            {
                break;
            }

            // wait for the button press
            readButtonPress();
            // send the answer
            sendAnswer(btnStateA, btnStateB, btnStateC);
        }
    }
}
