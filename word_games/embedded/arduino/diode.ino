#include <ezButton.h>
#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>
#include <Arduino.h>

#define DIODES 6

#define VCC 5.0
#define RESOLUTION 1024.0

// led strip
#define PIN 6
#define NUMPIXELS 11
#define TEST_DELAY 150
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

bool win = false;

int diodeStates[] = {0, 0, 0, 0, 0, 0};
int btnStates[] = {0, 0, 0, 0, 0, 0};
int diodePins[DIODES] = {7, 8, 9, 10, 11, 12};
ezButton diodeBtns[] = {
    ezButton(5),
    ezButton(7),
    ezButton(8),
    ezButton(9),
    ezButton(10),
    ezButton(11)};

void readDiodes()
{
    for (int i = 0; i < DIODES; i++)
    {
        // read diode state
        btnStates[i] = diodeBtns[i].getState();
    }
}
void sendJson()
{
    StaticJsonDocument<200> doc;
    JsonArray data = doc.createNestedArray("buttons");
    for (int i = 0; i < DIODES; i++)
    {
        data.add((int) btnStates[i]);
    }
    serializeJson(doc, Serial);
}
void setDiodes()
{
    for (int i = 0; i < DIODES; i++)
    {
        if (diodeStates[i] == 1)
        {
            pixels.setPixelColor(2*i, pixels.Color(255, 0, 0));
        }
        else
        {
            pixels.setPixelColor(2*i, pixels.Color(0, 255, 0));
        }
    }
    pixels.show();
    sendJson();
}

void setup()
{
    pixels.begin();
    pixels.setBrightness(10);
    pixels.show();
    for (int i = 0; i < DIODES; i++)
    {
        diodeBtns[i].setDebounceTime(50);
        // pixels.setPixelColor(2*i)
    }
    Serial.begin(9600);
    while (!Serial)
        continue;
    readDiodes();
    setDiodes();
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
        btnStates[i] = diodeBtns[i].getState(2);
    }
}

void loop()
{
    if (Serial.available() > 0)
    {
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, Serial);
        // if (error)
        // {
            // Serial.print(F("deserializeJson() failed: "));
            // Serial.println(error.c_str());
            // return;
        // }
        readJson(doc);
        setDiodes();
        delay(TEST_DELAY);
    }

    for (byte i = 0; i < DIODES; i++)
        diodeBtns[i].loop(); // MUST call the loop() function first
    readButtons();
    delay(TEST_DELAY);
    //   sendJson();
    //   delay(1000);
}
