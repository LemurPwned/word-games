#include <ArduinoJson.h>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define potPinRadial1 A1
#define potPinRadial2 A2
#define potPinLinear A3
#define VCC 5.0
#define RESOLUTION 1024

// led strip
#define PIN 12
#define NUMPIXELS 17
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

float potValRadial1 = 0;
float potValRadial2 = 0;
float potValLinear = 0;
int progress = 0;
bool win = false;

void setup()
{
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif
    pixels.begin();
//    pixels.setBrightness(15);
//    for (int i = 0; i < NUMPIXELS; i++)
//    {
//        pixels.setPixelColor(i, pixels.Color(255, 0, 0));
//    }
//    pixels.show();
    pinMode(potPinRadial1, INPUT);
    pinMode(potPinRadial2, INPUT);
    pinMode(potPinLinear, INPUT);
    setProgress(0);

    Serial.begin(9600);
    while (!Serial)
        continue;
}

void readJson(StaticJsonDocument<200> doc)
{
    win = doc["win"];
    progress = doc["progress"];
}

void setProgress(int progress)
{
    pixels.clear();
//    int lighted = floor((progress/100) * NUMPIXELS);
    for (int i = 0; i < NUMPIXELS; i++)
    {
        if (i < progress)
        {
            pixels.setPixelColor(i, pixels.Color(0, 0, 0));
        }
        else
        {
            pixels.setPixelColor(i, pixels.Color(0, 150, 0));
        }
        pixels.show();
    }
//    pixels.show();
}

void sendPositionJson(float x, float y, float z)
{
    StaticJsonDocument<200> doc;
    JsonArray data = doc.createNestedArray("position");
    data.add(x);
    data.add(y);
    data.add(z);
    serializeJsonPretty(doc, Serial);
}

double voltage2coordinate(float voltage)
{
    // convert voltage to coordinate
    // voltage = 0.0 -> coordinate = 0.0
    // voltage = 5.0 -> coordinate = 1.0
    return float(voltage) / float(RESOLUTION); //* (VCC / float(RESOLUTION));
}

void loop()
{

  for(int i=0; i<NUMPIXELS; i++) { // For each pixel...

    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    // Here we're using a moderately bright green color:
    pixels.setPixelColor(i, pixels.Color(0, 150, 0));

    pixels.show();   // Send the updated pixel colors to the hardware.

    delay(500); // Pause before next pass through loop
  }

//    if (Serial.available() > 0)
//    {
//        StaticJsonDocument<200> doc;
//        DeserializationError error = deserializeJson(doc, Serial);
//        if (error)
//        {
//            Serial.print(F("deserializeJson() failed: "));
//            Serial.println(error.c_str());
//            return;
//        }
//        readJson(doc);
//        setProgress(progress);
//        if (win)
//        {
//             Serial.println("Finished playing the calibrate game!");
//        }
//    }
//    potValRadial1 = analogRead(potPinRadial1);
//    potValRadial2 = analogRead(potPinRadial2);
//    potValLinear = analogRead(potPinLinear);
//    float radialD1 = voltage2coordinate(potValRadial1);
//    float radialD2 = voltage2coordinate(potValRadial2);
//    float linearD = voltage2coordinate(potValLinear);
//    sendPositionJson(radialD1, radialD2, linearD);
//    delay(1000);
}
