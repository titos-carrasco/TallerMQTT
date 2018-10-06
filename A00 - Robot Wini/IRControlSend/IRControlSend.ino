// Código IR Basado en IRremoteESP8266: IRsendDemo
// Utilizar IRecvDumpV2 para capturar los codigos

#include <ESP8266WiFi.h>
WiFiClient net;

#include <PubSubClient.h>
PubSubClient mqtt( net );

#include <IRremoteESP8266.h>
#include <IRsend.h>
IRsend irsend( 4 );   // 4 es pin D2

#define WIFI_SSID     "SSID de la red"
#define WIFI_PASS     "clave de la red"
#define MQTT_SERVER   "test.mosquitto.org"
#define MQTT_PORT     1883
#define MQTT_CLIENTID ( "Node_" + String( ESP.getChipId() ) )
#define MQTT_TOPIC    "rcr/ircontrol/01"

void setup() {
  Serial.begin(115200, SERIAL_8N1, SERIAL_TX_ONLY);  
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

  irsend.begin();

  mqtt.setServer( MQTT_SERVER, MQTT_PORT );
  mqtt.setCallback( doReceiveMessage );
  mqtt.connect( MQTT_CLIENTID.c_str() );
  mqtt.subscribe( MQTT_TOPIC, 0 );
}

void loop() {
  mqtt.loop();
  delay( 10 );
}

void doReceiveMessage( char *topic, byte *payload, unsigned int len  ) { 
  // secuencia de bytes como hex string: 00AABEO8...
  // los 4 primeros es un uint16 y asi sucesivamente 
  Serial.print( topic );
  Serial.print( " " );
  Serial.print( len );
  Serial.print( " " );
  Serial.write( payload, len );
  Serial.println();
  uint16_t rawData[ len/4 ];
  for( int j=0, i=0; i<len; ){
    unsigned int n3 = hexDigitToInt( payload[ i++ ] );
    unsigned int n2 = hexDigitToInt( payload[ i++ ] );
    unsigned int n1 = hexDigitToInt( payload[ i++ ] );
    unsigned int n0 = hexDigitToInt( payload[ i++ ] );
    rawData[ j++ ] = (((n3<<4)+n2)<<8) + ((n1<<4)+n0);
  }
  for( int i=0; i<len/4; i++ ){
    Serial.print( rawData[i]);
    Serial.print( ", " );   
  }
  Serial.println();
  
  irsend.sendRaw( rawData, len/4, 38 );  // Send a raw data at 38kHz.
}

int hexDigitToInt( char hex ){
  return hex<='9' ? hex - '0' : 10 + hex - 'A';
  return 1;
}

