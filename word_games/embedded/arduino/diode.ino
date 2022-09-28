#include <ezButton.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif
#include <ArduinoJson.h>
#include <Arduino.h>

#define DIODES 6

#define VCC 5.0
#define RESOLUTION 1024.0

// led strip
#define PIN 6
#define NUMPIXELS 6
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

bool win = false;

int diodeStates[] = {0, 0, 0, 0, 0, 0};
int diodePins[DIODES] = {7, 8, 9, 10, 11, 12};
ezButton diodeBtns[] = {
    ezButton(7),
    ezButton(8),
    ezButton(9),
    ezButton(10),
    ezButton(11),
    ezButton(12)};
void readDiodes()
{
    for (int i = 0; i < DIODES; i++)
    {
        // read diode state
        diodeStates[i] = diodeBtns[i].getState();
    }
}

void setDiodes()
{
    for (int i = 0; i < NUMPIXELS; i++)
    {
        if (diodeStates[i] == 1)
        {
            pixels.setPixelColor(i, pixels.Color(255, 255, 255));
        }
        else
        {
            pixels.setPixelColor(i, pixels.Color(0, 255, 0));
        }
    }
    pixels.show();
}

void setup()
{
    pixels.begin();
    pixels.setBrightness(10);
    pixels.show();
    for (int i = 0; i < DIODES; i++)
    {
        diodeBtns[i].setDebounceTime(50);
    }
    // read the last state
    //    readDiodes();
    Serial.begin(9600);
    while (!Serial)
        continue;
    readDiodes();
    setDiodes();
}

void sendJson()
{
    StaticJsonDocument<200> doc;
    JsonArray data = doc.createNestedArray("diodes");
    for (int i = 0; i < DIODES; i++)
    {
        data.add(diodeStates[i]);
    }
    serializeJsonPretty(doc, Serial);
}

void readJson(StaticJsonDocument<200> doc)
{
    win = doc["win"];
    for (int i = 0; i < DIODES; i++)
    {
        diodeStates[i] = doc["diodes"][i];
    }
}

void readButtons()
{
    for (byte i = 0; i < DIODES; i++)
    {
        diodeStates[i] = diodeBtns[i].getState();
    }
}
void loop()
{
    for (byte i = 0; i < DIODES; i++)
        diodeBtns[i].loop(); // MUST call the loop() function first
    readButtons();
    setDiodes();
    //   sendJson();
    //   delay(1000);
}
