

/*
Author : Morgan Mootoosamy
Date : 06/05/2024 (MM/DD/YYYY)
Updated : 07/09/2024 (MM/DD/YYYY)
Title : WiFi 2.4 GHz scanner
File : wifi_scan2.4.ino
*/




#include "WiFi.h"
#include <TinyGPS++.h>
#include <HardwareSerial.h>

TinyGPSPlus gps;


HardwareSerial gpsserial(1);  

void setup()
{
    Serial.begin(115200);
    gpsserial.begin(9600, SERIAL_8N1, 34, 12);;
    // Set WiFi to station mode and disconnect from an AP if it was previously connected.
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(10);
    
}

static void smartDelay(unsigned long ms)                
{
  unsigned long start = millis();
  do
  {
    while (gpsserial.available())
      gps.encode(gpsserial.read());
  } while (millis() - start < ms);
}
  
void loop()
{
       

  gps.location.lat(), 6;
  gps.location.lng(), 6;
  smartDelay(250);                                      
  
  int n = WiFi.scanNetworks();
  delay(50);
  
  if (n == 0) {
    Serial.print("[");
    Serial.print("{ \"id\" :\"");
    Serial.print("1");
    Serial.print("\", \"Lat\" :\"");
    Serial.print(gps.location.lat(), 6);
    Serial.print("\", \"Long\" :\"");
    Serial.print(gps.location.lng(), 6);
    smartDelay(250); 
    Serial.print("\", \"SSID\" :\"");
    Serial.print("None");
    Serial.print("\", \"RSSI\" :\"");
    Serial.print("-999");
    Serial.print("\", \"CH\" :\"");
    Serial.print("-1");
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
          if (i == 0) {
            Serial.print(gps.location.lat(), 6);
          }
          else{
            Serial.print("REPLACE");
          }
          Serial.print("\", \"Long\" :\"");
          if (i == 0) {
            Serial.print(gps.location.lng(), 6);
            smartDelay(250); 
          }
          else{
            Serial.print("REPLACE");
          }
          Serial.print("\", \"SSID\" :\"");
            if (WiFi.SSID(i).c_str() == ""){
              Serial.print("Unknown");
            }
            else{
              Serial.print(WiFi.SSID(i).c_str());
            }
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
              Serial.print("WPA/WPA2\"");
              break;
          case WIFI_AUTH_WPA2_ENTERPRISE:
              Serial.print("WPA2-EAP\"");
              break;
          case WIFI_AUTH_WPA3_PSK:
              Serial.print("WPA3\"");
              break;
          case WIFI_AUTH_WPA2_WPA3_PSK:
              Serial.print("WPA2/WPA3\"");
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
    Serial.print("],+");
    Serial.println("");
 
    // Delete the scan result to free memory for code below.
    WiFi.scanDelete(); 
}

