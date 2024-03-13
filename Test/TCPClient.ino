#include <Arduino.h>
#include <WiFi.h>
#include <string>
#include <dht11.h>
#define DHT11PIN 32

dht11 DHT11;

const char* ssid = "Linksys00339";//put your wifi ssid here
const char* password = "GoBoat33";//put your wifi password here.
const char* serverAddress = "192.168.1.10"; // TCP Server's IP ADDRESS Raspberry Pi IP: 192.168.1.10
const int serverPort = 8888; //server's port 

int RandNumber; //empty parameter to use with Random()
String UID = "ESP32"; //uniqe id, so its possible to sort them, ## current name is a placeholder
String Payload; //empty string parameter, later used for joining strings.

WiFiClient TCPclient;
void setup_wifi() { //Connect to wifi. While loop breaks when connected.
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED);
}

void setup_TCP() { //Connect to TCP server. While loop breaks when connected.
  TCPclient.connect(serverAddress, serverPort);
  while (TCPclient.connected() != true);
}

void setup() {
  esp_sleep_enable_timer_wakeup(60000000*5); // 60000000==1 min 
  Serial.begin(115200); //Makes it possible to print, remember to set IDE to 115200 baud. 
  setup_wifi(); // Runs setup_wifi function. 
  setup_TCP(); // Runs setup_TCP function.
  Serial.println("connected");
  
  int chk = DHT11.read(DHT11PIN);
  char Temp = DHT11.temperature;

  RandNumber = random(100);
  Payload = UID +","+ String(RandNumber) +","+ String(byte(Temp));

  TCPclient.write(Payload.c_str());
  Serial.print("Payload sent - ");

  Serial.println(Payload.c_str());
  delay(80);

  esp_deep_sleep_start();
}

void loop() { //Loop function is needed even if it is not used.
}
