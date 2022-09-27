#include <ArduinoJson.h>
#include <Arduino.h>

#define DIODES 6

#define VCC 5.0
#define RESOLUTION 1024.0

bool win = false;

int diodeStates[DIODES] = {0, 0, 0, 0, 0, 0};
int diodePins[DIODES] = {2, 3, 4, 5, 6, 7};
void setup()
{
    for (int i = 0; i < DIODES; i++)
    {
        pinMode(diodePins[i], INPUT);
    }

    Serial.begin(9600);
    while (!Serial)
        continue;
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

void readDiodes()
{
    for (int i = 0; i < DIODES; i++)
    {
        // read diode state
        diodeStates[i] = digitalRead(diodePins[i]);
    }
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
            readDiodes();
            sendJson();
        }
    }
}
