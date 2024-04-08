
//Include DHT Library To Receive Specific Values
#include "DHT.h"

//DHT11 Module Connected to Pin 2
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
//


void setup() 
{
  //LED: 3, 4 and 5
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);

  //13 Is the DC-Motor
  pinMode(13, OUTPUT);

  //Baud Rate is 9600
  Serial.begin(9600);

  //Start DHT to Begin Reading Values
  dht.begin();
}

void loop()
{
   //4 Second Delay Per Loop
   delay(4000);
   
   //Get Temperature and Humidity Values and Set Them As Floats
   float h = dht.readHumidity();
   float t = dht.readTemperature();

   int analogueValue = analogRead(A0); //analogueValue reads analog input A0 value
   
   //Set LED Brightness
   int led_brightness = analogueValue * (255 / 1023.0); //this scales the value between 0-255

   //Print Potentiometer, Humidity and Temperature Values
   Serial.println(analogueValue);
   Serial.println(h);
   Serial.println(t);


   //Check if there is serial input data available 
   if (Serial.available()>0)
      {
        //Read serial input and Set to Activate, LED's and DC Motor
        int activate_component = Serial.read();
        
        //1 - 6 = LED
        //7 - 8 = DC Motor

        if (activate_component == '1')
        {
          analogWrite(3, led_brightness); //Activate Based on Potentiometer Value
        }
        else if (activate_component == '2')
        {
          analogWrite(3,0);
        }
        else if (activate_component == '3')
        {
          analogWrite(4, led_brightness); //Activate Based on Potentiometer Value
        }
        else if (activate_component == '4')
        {
          analogWrite(4,0);
        }
        else if (activate_component == '5')
        {
          analogWrite(5, led_brightness); //Activate Based on Potentiometer Value
        }
        else if (activate_component == '6')
        {
          analogWrite(5,0);
        }
        else if (activate_component == '7')
        {
          analogWrite(13, 255); //Set the DC Motor To HIGH (255)
        }
        else if (activate_component == '8')
        {
          analogWrite(13,0); //Set the DC Motor To LOW (0)
        }
      }    
}
