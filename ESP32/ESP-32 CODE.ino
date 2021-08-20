#include <WiFi.h>
#include <HTTPClient.h>
#include "BluetoothSerial.h"
#include "ELMduino.h"

BluetoothSerial SerialBT;
#define ELM_PORT   SerialBT
#define DEBUG_PORT Serial
ELM327 myELM327;
const char* ssid = "vivo 1919";
const char* password = "012345678";

int rpm = 10;
int speedd = 20;

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;

void setup() {
  Serial.begin(115200); 
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting...");
  }
 
  Serial.println("Connected successfully.");
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");

#if LED_BUILTIN
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
#endif
  DEBUG_PORT.begin(115200);
  SerialBT.setPin("1234");
  ELM_PORT.begin("ArduHUD", true);
  
  if (!ELM_PORT.connect("OBD2"))
  {
    DEBUG_PORT.println("Couldn't connect to OBD scanner - Phase 1");
    while(1);
  }

  if (!myELM327.begin(ELM_PORT, true, 2000))
  {
    Serial.println("Couldn't connect to OBD scanner - Phase 2");
    while (1);
  }

    Serial.println("Connected to ELM327");
}

void loop() {
  //Send an HTTP POST request every 10 minutes
   if (myELM327.status == ELM_SUCCESS)
   {
      float tempRPM = myELM327.rpm();
      float tempSpeed = myELM327.kph();
      rpm = (int)tempRPM;
      speedd=(int)tempSpeed;
      Serial.print("RPM: "); Serial.println(rpm);
      if (WiFi.status() != WL_CONNECTED) {
        Serial.println("wifi error");
      } 
      else {
        
        HTTPClient wlanhttp;

        wlanhttp.begin("http://192.168.29.244:5000/getdata?speed="+String(speedd)+"&rpm="+String(rpm));
//        wlanhttp.begin("http://192.168.137.71:5000/getdata?rpm="+String(rpm));
        
        int httpcode = wlanhttp.GET();
        Serial.println(httpcode);
    
        if(httpcode>0){
    
          String payload = wlanhttp.getString();
          Serial.println(httpcode);
          Serial.println(payload);
          }
    
        else {
          Serial.println("error on HTTP request");
          }
        wlanhttp.end();  
        delay(3000);
      }
   }
   else
    myELM327.printError();
   }
