#include <ArduinoJson.h>
#include <Arduino.h>

#define potPinRadial1 A4
#define potPinRadial2 A5
#define potPinLinear A6
#define VCC 5.0
#define RESOLUTION 1024.0

float potValRadial1 = 0;
float potValRadial2 = 0;
float potValLinear = 0;

bool win = false;

void setup()
{
    Serial.begin(9600);
    pinMode(potPinRadial1, INPUT);
    pinMode(potPinRadial2, INPUT);
    pinMode(potPinLinear, INPUT);
    while (!Serial)
        continue;
}

bool readJson(StaticJsonDocument<200> doc)
{
    return doc["win"];
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
    return float(voltage) * (VCC / float(RESOLUTION));
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
            win = readJson(doc);
            if (win)
            {
                // Serial.println("Finished playing the calibrate game!");
                break;
            }
        }
        potValRadial1 = analogRead(potPinRadial1);
        potValRadial2 = analogRead(potPinRadial2);
        potValLinear = analogRead(potPinLinear);
        float radialD1 = voltage2coordinate(potValRadial1);
        float radialD2 = voltage2coordinate(potValRadial2);
        float linearD = voltage2coordinate(potValLinear);
        sendPositionJson(radialD1, radialD2, linearD);
    }
}
