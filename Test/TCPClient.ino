#include <Arduino.h>
#include <WiFi.h>
#include <string>
#include <dht11.h>
#define DHT11PIN 32

dht11 DHT11;

//segmentation 

const char* ssid = "Linksys00339";//put your wifi ssid here
const char* password = "GoBoat33";//put your wifi password here.
const char* serverAddress = "192.168.1.10"; // TCP Server's IP ADDRESS
const int serverPort = 8888; //server's port 
//char* payload = "111112222211111222221111122222111112";

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
  Serial.begin(115200); //Makes it possible to print, remember to set IDE to 115200 baud. 
  setup_wifi(); // Runs setup_wifi function. 
  setup_TCP(); // Runs setup_TCP function.
  Serial.println("connected");
}

void loop() { //Loop function is mandatory even if it is not used.
  setup_TCP(); // Runs setup_TCP function.
  delay(2000); // Time specified in milliseconds.

  int chk = DHT11.read(DHT11PIN);
  char temp = DHT11.temperature;
  TCPclient.write(byte(temp));

  Serial.print("payload sent - ");
  Serial.println(byte(temp));
}
