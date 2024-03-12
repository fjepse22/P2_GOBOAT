#include <Arduino.h>
#include <WiFi.h>
#include <string>
#include <dht11.h>
#define DHT11PIN 32

dht11 DHT11;

const char* ssid = "Linksys00339";//put your wifi ssid here
const char* password = "GoBoat33";//put your wifi password here.
const char* serverAddress = "192.168.1.140"; // TCP Server's IP ADDRESS Raspberry Pi IP: 192.168.1.10
const int serverPort = 8888; //server's port 
int RandNumber;
int TempTest = 25;
String UID = "ESP32";
String Payload;


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
  delay(2000); // Time specified in milliseconds.
  setup_TCP(); // Runs setup_TCP function.

  int chk = DHT11.read(DHT11PIN); //Reads information from pin.
  char Temp = DHT11.temperature;

  RandNumber = random(100); // Random number from 0 to 100.
  Payload = UID +","+ String(RandNumber) +","+ String(byte(Temp)); // combines UID, RandNumber and Temperture.
  
  TCPclient.write(Payload.c_str()); // sends the Payload
  Serial.print("Payload sent - "); // prints the Payload
  Serial.println(Payload.c_str()); 

}
