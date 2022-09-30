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

ezButton btns[] = {
    ezButton(2),
    ezButton(14),
    ezButton(15),
};
int btnStates[3] = {0, 0, 0};

// led strip
#define PIN_A 10
#define PIN_B 11
#define PIN_C 12
#define NUMPIXELS 10
Adafruit_NeoPixel pixelsA(NUMPIXELS, PIN_A, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixelsB(NUMPIXELS, PIN_B, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixelsC(NUMPIXELS, PIN_C, NEO_GRB + NEO_KHZ800);
#define TEST_DELAY 200

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
    Serial.begin(9600);
    while (!Serial)
        continue;
    pixelsA.begin();
    pixelsB.begin();
    pixelsC.begin();

    uint8_t data[] = {0xff, 0xff, 0xff, 0xff};
    displayA.setBrightness(0x0f);
    displayB.setBrightness(0x0f);
    displayC.setBrightness(0x0f);
    displayA.setSegments(data);
    displayB.setSegments(data);
    displayC.setSegments(data);
    
    setProgress(15);
    displayNumber(10, displayA);
    displayNumber(892, displayB);
    displayNumber(2731, displayC);

    for (int i = 0; i < 3; i++)
    {
        btns[i].setDebounceTime(50);
    }

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
    if (!win)
    {
        displayNumber(numberA, displayA);
        displayNumber(numberA, displayB);
        displayNumber(numberC, displayC);
    }
    else
    {
        displayA.setSegments(SEG_DONE);
        displayB.setSegments(SEG_DONE);
        displayC.setSegments(SEG_DONE);
    }
    setProgress(score);
}


void setProgress(int progress)
{
  pixelsA.clear();
  pixelsB.clear();
  pixelsC.clear();
    for (int i = 0; i < NUMPIXELS; i++ ){
        if (i < progress)
            pixelsA.setPixelColor(i, pixelsA.Color(0, 255, 0));
        else
            pixelsA.setPixelColor(i, pixelsA.Color(255, 0, 0));
    }
    pixelsA.show();
    int secondProgress = progress - 10;
    for (int i = 0; i < NUMPIXELS; i++ ){
        if (i < secondProgress)
            pixelsB.setPixelColor(i, pixelsB.Color(0, 255, 0));
        else
            pixelsB.setPixelColor(i, pixelsB.Color(255, 0, 0));
    }
    pixelsB.show();
    int thirdProgress = progress - 20;
    for (int i = 0; i < NUMPIXELS; i++ ){
        if (i < thirdProgress)
            pixelsC.setPixelColor(i, pixelsC.Color(0, 255, 0));
        else
            pixelsC.setPixelColor(i, pixelsC.Color(255, 0, 0));
    }
    pixelsC.show();  
    // Serial.println("#START");
    // Serial.println(secondProgress);
    // Serial.println(thirdProgress);
    // Serial.println("#END");
}


void sendJson(int state)
{
    StaticJsonDocument<100> doc;
    doc["ans"] = state;
    serializeJson(doc, Serial);
}


void readSerial(){
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
    }
}

void loop()
{
  // for (int i = 0; i < 30; i++){
  //   setProgress(i);
  //   delay(1500);
  //   Serial.println(i);
  // }
  readSerial();
  delay(TEST_DELAY);
  for (byte i = 0; i < 3; i++)
    btns[i].loop(); // MUST call the loop() function first

  for (byte i = 0; i < 3; i++){
    if (btns[i].isPressed()){
      // Serial.print(i);
      // Serial.print("is pressed\n");      
      sendJson(i);
      delay(TEST_DELAY);
    }
  }
}
    