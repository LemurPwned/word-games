#include <ArduinoJson.h>
#include <TM1637Display.h>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#include <ezButton.h>

#define CLK_A 7
#define CLK_B 5
#define CLK_C 3

#define DIO_A 8
#define DIO_B 6
#define DIO_C 4

#define BTN_A 6
#define BTN_B 7
#define BTN_C 8

ezButton btns[] = {
    ezButton(4),
    ezButton(3),
    ezButton(2),
};
int btnStates[3] = {0, 0, 0};

// led strip
#define PIN 12
#define NUMPIXELS 11
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define TEST_DELAY 2000

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

TM1637Display displayA(CLK_A, DIO_A);
TM1637Display displayB(CLK_B, DIO_B);
TM1637Display displayC(CLK_C, DIO_C);

void readBtns()
{
    for (int i = 0; i < 3; i++)
    {
        // read diode state
        btnStates[i] = btns[i].getState();
    }
}

void setup()
{
    pixels.begin();
    pixels.setBrightness(10);
    for (int i = 0; i < NUMPIXELS; i++)
    {
        pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    }
    pixels.show();
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

    setProgress(0);
    displayNumber(10, displayA);
    displayNumber(892, displayB);
    displayNumber(2731, displayC);

    for (int i = 0; i < 3; i++)
    {
        btns[i].setDebounceTime(50);
    }
    Serial.begin(9600);
    while (!Serial)
        continue;
}

void displayNumber(int number, TM1637Display display)
{
    // leading zero is set to false
    display.showNumberDec(number, false);
    delay(TEST_DELAY);
}

void readJson(StaticJsonDocument<200> doc)
{
    win = doc["win"];
    numberA = doc["numbers"][0];
    numberB = doc["numbers"][1];
    numberC = doc["numbers"][2];
    score = doc["score"];
    if (!win)
    {

        displayNumber(numberA, displayA);
        displayNumber(numberB, displayB);
        displayNumber(numberC, displayC);
    }
    else
    {
        displayA.setSegments(SEG_DONE);
        displayB.setSegments(SEG_DONE);
        displayC.setSegments(SEG_DONE);
    }
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

void setProgress(int progress)
{

    for (int i = 0; i < NUMPIXELS; i++)
    {
        if (i < progress)
        {
            pixels.setPixelColor(i, pixels.Color(255, 255, 255));
        }
        else
        {
            pixels.setPixelColor(i, pixels.Color(0, 0, 0));
        }
    }
    pixels.show();
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

void sendJson()
{
    StaticJsonDocument<200> doc;
    JsonArray data = doc.createNestedArray("btns");
    for (int i = 0; i < 3; i++)
    {
        data.add(btnStates[i]);
    }
    serializeJsonPretty(doc, Serial);
}

void loop()
{
    for (byte i = 0; i < 3; i++)
        btns[i].loop(); // MUST call the loop() function first


    readBtns();
    sendJson();
    delay(1000);

    // pixels.begin();
    // pixels.setBrightness(10);
    // for (int i = 0; i < NUMPIXELS; i++)
    // {
    //     pixels.setPixelColor(i, pixels.Color(255, 0, 0));
    // }
    // pixels.show();
    // delay(TEST_DELAY);


    // if (Serial.available() > 0)
    // {
    //     StaticJsonDocument<200> doc;
    //     DeserializationError error = deserializeJson(doc, Serial);
    //     if (error)
    //     {
    //         Serial.print(F("deserializeJson() failed: "));
    //         Serial.println(error.c_str());
    //         return;
    //     }
    //     readJson(doc);
    //     setProgress(score);
    //     if (win)
    //     {
    //         break;
    //     }

    //     // wait for the button press
    //     readButtonPress();
    //     // send the answer
    //     sendAnswer(btnStateA, btnStateB, btnStateC);
    // }
}
