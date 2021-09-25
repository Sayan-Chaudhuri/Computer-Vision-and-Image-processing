#include <ESP8266WiFi.h>
#include<WiFiClient.h>
#include <ESP8266mDNS.h>
const char* ssid = "OPPO F17"; // Write here your router's username
const char* password = "khichudi"; // Write here your router's passward

WiFiServer server(80);
/* define L298N or L293D motor control pins */

int leftMotorForward = 2;     /* GPIO2(D4) -> IN3   */

int rightMotorForward = 15;   /* GPIO15(D8) -> IN1  */

int leftMotorBackward = 0;    /* GPIO0(D3) -> IN4   */

int rightMotorBackward = 13;  /* GPIO13(D7) -> IN2  */



/* define L298N or L293D enable pins */

int rightMotorENB = 14; /* GPIO14(D5) -> Motor-A Enable */

int leftMotorENB = 12;  /* GPIO12(D6) -> Motor-B Enable */

void setup() {
  // put your setup code here, to run once:
  pinMode(leftMotorForward, OUTPUT);

  pinMode(rightMotorForward, OUTPUT);

  pinMode(leftMotorBackward, OUTPUT);  

  pinMode(rightMotorBackward, OUTPUT);


  /* initialize motor enable pins as output */

  pinMode(leftMotorENB, OUTPUT);

  pinMode(rightMotorENB, OUTPUT);
  
  Serial.begin(9600);
       delay(10);
               
       Serial.println("Connecting to ");
       Serial.println(ssid); 
       WiFi.mode(WIFI_STA);
       WiFi.begin(ssid, password); 
       while (WiFi.status() != WL_CONNECTED) 
          {
            delay(500);
            Serial.println("No Connection");
          }
      Serial.println("");
      Serial.println("WiFi connected"); 
      Serial.println(WiFi.localIP()); 
  // Print the IP address
      server.begin();
     // MDNS.addService("http", "tcp", 80);
      //client=server.available();
}

void loop() {
  // put your main code here, to run repeatedly:
    WiFiClient client=server.available();
    if(client)
    {
      // Serial.println("Hello");
      while(client.connected())
      {
        if(client.available())
        {
           String req=client.readStringUntil('\n');
           if(req=="5")
           {
              move_forward();
           }
           else if(req=="4")
           {
              move_backward();
           }
           else if(req=="3")
           {
              move_right();
           }
           else if(req=="2")
           {
               move_left()
           }
           else if(req=="1")
           {
               stop_movement();
           }
           Serial.println(req);
           client.print("Success");
        }
      }
      client.stop();
      stop_movement();
      Serial.println("Client Disconnected");
    }
    
    
}

void move_forward(void)  

{

  digitalWrite(leftMotorENB,HIGH);

  digitalWrite(rightMotorENB,HIGH);

  digitalWrite(leftMotorForward,HIGH);

  digitalWrite(rightMotorForward,HIGH);

  digitalWrite(leftMotorBackward,LOW);

  digitalWrite(rightMotorBackward,LOW);

}

void move_backward(void)  

{

  digitalWrite(leftMotorENB,HIGH);

  digitalWrite(rightMotorENB,HIGH);

  digitalWrite(leftMotorBackward,HIGH);

  digitalWrite(rightMotorBackward,HIGH);

  digitalWrite(leftMotorForward,LOW);

  digitalWrite(rightMotorForward,LOW);

}




void move_left(void)  

{

  digitalWrite(leftMotorENB,HIGH);

  digitalWrite(rightMotorENB,HIGH);

  digitalWrite(leftMotorForward,LOW);

  digitalWrite(rightMotorForward,HIGH);

  digitalWrite(rightMotorBackward,LOW);

  digitalWrite(leftMotorBackward,HIGH);  

}



void move_right(void)  

{

  digitalWrite(leftMotorENB,HIGH);

  digitalWrite(rightMotorENB,HIGH);

  digitalWrite(leftMotorForward,HIGH);

  digitalWrite(rightMotorForward,LOW);

  digitalWrite(rightMotorBackward,HIGH);

  digitalWrite(leftMotorBackward,LOW);

}




void stop_movement(void)  

{

  digitalWrite(leftMotorENB,LOW);

  digitalWrite(rightMotorENB,LOW);

  digitalWrite(leftMotorForward,LOW);

  digitalWrite(leftMotorBackward,LOW);

  digitalWrite(rightMotorForward,LOW);

  digitalWrite(rightMotorBackward,LOW);

}
