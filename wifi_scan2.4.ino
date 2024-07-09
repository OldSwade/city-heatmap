#include "WiFi.h"
//#include <TinyGPS++.h>
#include <SoftwareSerial.h>

//TinyGPSPlus gps;

//static const int RXPin = 12, TXPin = 34;
//static const uint32_t GPSBaud = 4800;

float latitude = -1;
float longitude = -1;
float altitude = -1;

//SoftwareSerial ss(RXPin, TXPin);

void setup()
{
    Serial.begin(115200);
    //ss.begin(GPSBaud);
    // Set WiFi to station mode and disconnect from an AP if it was previously connected.
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(10);
    
}
  
void loop()
{     
      /*while (ss.available() > 0){
        //Serial.print(ss.read());
        //Serial.print(gps.encode(ss.read()));
        //Serial.print(gps.charsProcessed());
        //Serial.print(gps.location.isValid());
        if (gps.encode(ss.read()))
        {
          
          if (gps.location.isValid())
          {
            float latitude = (gps.location.lat(),6);
            float longitude = (gps.location.lng(),6);
          }
          
        }
          
      if (millis() > 5000 && gps.charsProcessed() < 10)
      {
        while(true);
      }
    }
    Serial.print("Latitude : ");
    Serial.print(gps.location.lat(),6);
    Serial.println("");
    Serial.print("Longitude : ");
    Serial.print(gps.location.lng(),6);
    Serial.println("");
    */

    // WiFi.scanNetworks will return the number of networks found.

    int n = WiFi.scanNetworks();
    delay(50);
    
    if (n == 0) {
      Serial.print("[");
      Serial.print("{ \"id\" :\"");
      Serial.print("None");
      Serial.print("\", \"Lat\" :\"");
      Serial.print(latitude);
      Serial.print("\", \"Long\" :\"");
      Serial.print(longitude);
      Serial.print("\", \"SSID\" :\"");
      Serial.print("None");
      Serial.print("\", \"RSSI\" :\"");
      Serial.print("None");
      Serial.print("\", \"CH\" :\"");
      Serial.print("None");
      Serial.print("\", \"Enc\" :\"");
      Serial.print("None");
      Serial.print("\", \"BSSID\" :\"");
      Serial.print("None\"}");
    } else { 
      Serial.print("[");
        for (int i = 0; i < n; ++i) {
            Serial.print("{ \"id\" :\"");
            Serial.print(i+1);
            Serial.print("\", \"Lat\" :\"");
            Serial.print(latitude);
            Serial.print("\", \"Long\" :\"");
            Serial.print(longitude);
            Serial.print("\", \"SSID\" :\"");
            Serial.print(WiFi.SSID(i).c_str());
            Serial.print("\", \"RSSI\" :\"");
            Serial.print(WiFi.RSSI(i));
            Serial.print("\", \"CH\" :\"");
            Serial.print(WiFi.channel(i));
            Serial.print("\", \"Enc\" :\"");
            switch (WiFi.encryptionType(i))
            {
            case WIFI_AUTH_OPEN:
                Serial.print("open\"");
                break;
            case WIFI_AUTH_WEP:
                Serial.print("WEP\"");
                break;
            case WIFI_AUTH_WPA_PSK:
                Serial.print("WPA\"");
                break;
            case WIFI_AUTH_WPA2_PSK:
                Serial.print("WPA2\"");
                break;
            case WIFI_AUTH_WPA_WPA2_PSK:
                Serial.print("WPA+WPA2\"");
                break;
            case WIFI_AUTH_WPA2_ENTERPRISE:
                Serial.print("WPA2-EAP\"");
                break;
            case WIFI_AUTH_WPA3_PSK:
                Serial.print("WPA3\"");
                break;
            case WIFI_AUTH_WPA2_WPA3_PSK:
                Serial.print("WPA2+WPA3\"");
                break;
            case WIFI_AUTH_WAPI_PSK:
                Serial.print("WAPI\"");
                break;
            default:
                Serial.print("unknown\"");
            }
            Serial.print(", \"BSSID\" :\"");
            Serial.print(WiFi.BSSIDstr(i));
            if (i+1 == n){
              Serial.print("\"}");
            }
            else{
              Serial.print("\"},");
            }
            delay(10);
        }
    }
    Serial.print("],");
    Serial.println("");
 
    // Delete the scan result to free memory for code below.
    WiFi.scanDelete(); 
}