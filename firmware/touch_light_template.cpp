#include "neopixel.h"
#include "application.h"

// NEOPIXEL
#define PIXEL_PIN D2
#define PIXEL_COUNT 12
#define PIXEL_TYPE WS2812B

Adafruit_NeoPixel strip(PIXEL_COUNT, PIXEL_PIN, PIXEL_TYPE);


// TIMING
#define LIGHT_ON_TIME 5*60*1000 // 5 minutes
unsigned long tStartLightTime;
bool bTurnLightsOn;


// COLOR
uint8_t myRed=0, myBlue=0, myGreen=0;


// INTERNET
TCPClient myTCP;
String hostname = ""; // device specific
byte data[11];


// BUTTON
#define BUTTON_PIN D4
#define BUTTON_DEBOUNCE_TIME 30*1000
bool bButtonPressed, bDoubleTapButton;
unsigned long tButtonPressTime;

// FUNCTIONS
int setLedColor(String color); 
void lampTouched();
void pulseRing();
void sendGetRequest();
void setMyColor();
void InitColor();
void lampTouched();
void turnLightsOff();

void setup() {

    // TODO:
    // 1. Choose what type of mechanical action triggers this
    // 2. write interrupt handler for that
    // 3. add wraparound check for timers? eh....

    pinMode(PIXEL_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLDOWN);

    attachInterrupt(BUTTON_PIN, lampTouched, FALLING);

    Particle.function("setColor", setLedColor);
    Particle.function("")

    // TODO: get color from server on startup
    InitColor();
    strip.begin();
}

void loop() {
    // LED on timer
    if (bTurnLightsOn) {
        if ((millis() - tStartLightTime) > LIGHT_ON_TIME) {
            bTurnLightsOn = false;
            turnLightsOff();
        }
    }

    // debounce timer
    if (bButtonPressed) {
        if ((millis() - tButtonPressTime) > BUTTON_DEBOUNCE_TIME) {
            bButtonPressed = false;
            attachInterrupt(BUTTON_PIN, lampTouched, FALLING);
        }
    }
    
    // "re-tap" timer
}

/**
 * Converts Particle POST function arguement to local uint32_t
 * @param String color in form "RRR,GGG,BBB"
 */
int setLedColor(String color) {
    // lazy validator
    if (color.length() != 11) {
        return -1;
    }

    // convert string to integer values
    uint8_t r, g, b;
    String temp;
    
    temp = color.substring(0,3);
    r = (uint8_t) temp.toInt();

    temp = color.substring(4,7);
    g = (uint8_t) temp.toInt();

    temp = color.substring(8);
    b = (uint8_t) temp.toInt();

    // set all pixels to that color
    uint8_t i;
    for (i = 0; i < PIXEL_COUNT; i++)
    {
        strip.setPixelColor(i, r, g, b);
    }

    // show my color [debugging]
    pulseRing();

    return 1;
}


// TODO: Karen
// Get request code is copied from internet
// https://community.particle.io/t/tcp-client-question/11597/5
void InitColor() {
    // sendGetRequest();
}


void sendGetRequest(const char * server, const char * url)
{
    if (myTCP.connect(server, 80)) {
        myTCP.print("GET ");
        myTCP.print(url);
        myTCP.println(" HTTP/1.0");
        myTCP.println("Connection: close");
        myTCP.print("Host: ");
        myTCP.println(server);
        myTCP.println("Accept: text/html, text/plain");
        myTCP.println();
        myTCP.flush();  // this is just for safety's sake, no real purpose
    } 
}


void lampTouched() {
    if (bButtonPressed == false)
    {
        setMyColor();
        bButtonPressed = true;
        tButtonPressTime = millis();

        detachInterrupt(BUTTON_PIN);

        if (bTurnLightsOn == false) {
            pulseRing();
        }
        else {
            // ok this is not great
            // probably can fix this with a software timer later
            // but for now we'll assume you don't press back within 120ms
            turnLightsOff();
            delay(100); // UGHHHHHHHHH so bad
            setMyColor();
            pulseRing();
        }
    }
}

void setMyColor() {
    uint8_t i;
    for (i = 0; i < PIXEL_COUNT; i++)
    {
        strip.setPixelColor(i, myRed, myGreen, myBlue);
    }
}

void pulseRing() {
    bTurnLightsOn = true;
    tStartLightTime = millis();
    strip.show();
}


void turnLightsOff() {
    uint8_t i;
    for (i = 0; i < PIXEL_COUNT; i++)
    {
        strip.setPixelColor(i, 0, 0, 0);
    }
    strip.show();
}