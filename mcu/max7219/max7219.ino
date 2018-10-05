#include <ESP8266WiFi.h>
WiFiClient net;

#include <PubSubClient.h>
PubSubClient mqtt( net );

/* DataIn: D3, CLK: D4, LOAD/CS: D5, # de matrices */
#include "LedControl.h"
LedControl lc=LedControl( D3, D4,D5, 1 );

#define WIFI_SSID     "Raspi01"
#define WIFI_PASS     "raspi01ipst"
#define MQTT_SERVER   "tron-ipst.freeddns.org"
#define MQTT_PORT     1883
#define MQTT_CLIENTID ( "Node_" + String( ESP.getChipId() ) )
#define MQTT_TOPIC    "rcr/matrix"

void setup() {
  Serial.begin(115200);  
  Serial.println();
  Serial.println();

  WiFi.mode( WIFI_STA );
  WiFi.setAutoConnect( true );
  WiFi.begin( WIFI_SSID, WIFI_PASS );
  Serial.print( "Conectando a la WiFi: ." );
  while( WiFi.status() != WL_CONNECTED ) {
    Serial.print( "." );
    delay( 500 );
  }
  Serial.println( " Conectado" );

  lc.shutdown(0,false);
  lc.setIntensity(0,8);
  lc.clearDisplay(0);

  mqtt.setServer( MQTT_SERVER, MQTT_PORT );
  mqtt.setCallback( doReceiveMessage );
  mqtt.connect( MQTT_CLIENTID.c_str() );
  mqtt.subscribe( MQTT_TOPIC, 0 );
}

void loop() {
  mqtt.loop();
  delay( 10 );
}

const byte IMAGES[][8] = {
{
  B00111000,
  B01000100,
  B01000100,
  B01000100,
  B01000100,
  B01000100,
  B01000100,
  B00111000
},{
  B00010000,
  B00110000,
  B00010000,
  B00010000,
  B00010000,
  B00010000,
  B00010000,
  B00111000
},{
  B00111000,
  B01000100,
  B00000100,
  B00000100,
  B00001000,
  B00010000,
  B00100000,
  B01111100
},{
  B00111000,
  B01000100,
  B00000100,
  B00011000,
  B00000100,
  B00000100,
  B01000100,
  B00111000
},{
  B00000100,
  B00001100,
  B00010100,
  B00100100,
  B01000100,
  B01111100,
  B00000100,
  B00000100
},{
  B01111100,
  B01000000,
  B01000000,
  B01111000,
  B00000100,
  B00000100,
  B01000100,
  B00111000
},{
  B00111000,
  B01000100,
  B01000000,
  B01111000,
  B01000100,
  B01000100,
  B01000100,
  B00111000
},{
  B01111100,
  B00000100,
  B00000100,
  B00001000,
  B00010000,
  B00100000,
  B00100000,
  B00100000
},{
  B00111000,
  B01000100,
  B01000100,
  B00111000,
  B01000100,
  B01000100,
  B01000100,
  B00111000
},{
  B00111000,
  B01000100,
  B01000100,
  B01000100,
  B00111100,
  B00000100,
  B01000100,
  B00111000
}};

void doReceiveMessage( char *topic, byte *payload, unsigned int len  ) { 
  if( len!= 1 ) return;
  char c = payload[0];
  if( c<'0' || c>'9' ) return;
  int d = c - '0';
  
  Serial.println( d );
  for( int i=0; i<8; i++ )
    lc.setColumn( 0, i, IMAGES[d][7-i] );
}
