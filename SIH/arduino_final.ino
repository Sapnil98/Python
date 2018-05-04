#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

const char* ssid = "";
const char* password = "";

WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on
char incomingPacket[1024];  // buffer for incoming packets
char  replyPacket[] = "Hi there! Got the message :-)";  // a reply string to send back
char stat[];
IPAddress remote_ip;
int remote_port;

void setup()
{
  Serial.begin(115200);
  Serial.println();
  
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println(" connected");

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

// ---------------------------------------------READ THE FIRST PACKET TO START---------------------------------
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    
    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    
    int len = Udp.read(incomingPacket, 1024);
    remote_ip=Udp.remoteIP();
    remote_port=Udp.remotePort();
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
//-------------------------------------------------------------------------------------------------------------
}


void loop()
{   
// -------------------------------------- SENDING PACKET ----------------------------------------------------

    if (incomingPacket=="start")      // send back a reply, to the IP address and port we got the packet from
    {
      
    
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      Udp.write("message");
      Udp.endPacket();
      Serial.println("Reply done");
      delay(3000);
      stat="done sending";
    }
//----------------------------------------- RECEIVING PACKET ---------------------------------------------
    if(stat == "done sending")
    {
      int packetSize = Udp.parsePacket();
      if (packetSize)
    {
      // receive incoming UDP packets
    
      //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    
      int len = Udp.read(incomingPacket, 1024);
      if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
    }
  }
//--------------------------------------------------------------------------------------------------------------
}

