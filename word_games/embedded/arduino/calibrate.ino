#include <ArduinoJson.h>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define potPinRadial1 A4
#define potPinRadial2 A2
#define potPinLinear A3
#define VCC 5.0
#define RESOLUTION 1024

// led strip
#define PIN 12
#define NUMPIXELS 17
#define TEST_DELAY 300
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

float potValRadial1 = 0;
float potValRadial2 = 0;
float potValLinear = 0;
float progress = 0.0;
bool win = false;

void setup()
{
    pixels.begin();
    pinMode(potPinRadial1, INPUT);
    pinMode(potPinRadial2, INPUT);
    pinMode(potPinLinear, INPUT);
    setProgress(0.);

    Serial.begin(9600);
    while (!Serial)
        continue;
}

void readJson(StaticJsonDocument<200> doc)
{
    win = doc["win"];
    progress = doc["progress"];
    setProgress(progress);
}

void setProgress(float progress)
{
   pixels.clear();
   int lighted = floor((progress/100) * NUMPIXELS);
    for (int i = 0; i < NUMPIXELS; i++)
    {
        if (i < lighted)
        {
            pixels.setPixelColor(i, pixels.Color(0, 255, 0));
        }
        else
        {
            pixels.setPixelColor(i, pixels.Color(255, 0, 0));
        }
        // pixels.show();
    }
   pixels.show();
}

void sendPositionJson(float x, float y, float z)
{
    StaticJsonDocument<200> doc;
    JsonArray data = doc.createNestedArray("position");
    data.add(x);
    data.add(y);
    data.add(z);
    serializeJson(doc, Serial);
}

double voltage2coordinate(float voltage)
{
    // convert voltage to coordinate
    // voltage = 0.0 -> coordinate = 0.0
    // voltage = 5.0 -> coordinate = 1.0
    return float(voltage) / float(RESOLUTION);
}

void loop()
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
       delay(TEST_DELAY);
      //  setProgress(prog
  }
  else{
    potValRadial1 = analogRead(potPinRadial1);
    potValRadial2 = analogRead(potPinRadial2);
    potValLinear = analogRead(potPinLinear);
    float radialD1 = 1.0 - voltage2coordinate(potValRadial1);
    float radialD2 = 1.0 - voltage2coordinate(potValRadial2);
    float linearD = 1.0 - voltage2coordinate(potValLinear);
    sendPositionJson(radialD1, radialD2, linearD);
    delay(TEST_DELAY);
  }
}
