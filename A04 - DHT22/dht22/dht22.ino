// librerías mínimas requeridas
#include <Arduino.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// la version 6 de esta libreria esta en beta. instalar la 5
#include <ArduinoJson.h>

// objetos para la WiFi y el broker MQTT
WiFiClient wiFiClient;
PubSubClient mqtt( wiFiClient );

// datos de la WiFi
#define WIFI_SSID       "Raspi01"
#define WIFI_PASS       "raspi01ipst"

// datos del broker MQTT
#define MQTT_SERVER     "tron-ipst.freeddns.org"
#define MQTT_PORT       1883
String  MQTT_CLIENTID = "Node_" + String( ESP.getChipId() );
#define MQTT_TOPIC      "rcr/dht22"

// control del código
#define MODO_MQTT       1       // 0: modo testing, 1: modo MQTT
#define MS_SLEEP        5000    // milisegundos de espera entre ciclos
#define DEEP_SLEEP      0       // 0: no usar DeepSleep, 1: usar DeepSleep

// colocar aquí definiciones para su programa
#include "DHT.h"
DHT dht( D3, DHT22 );

void setup()
{
  // inicia monitor serial
  Serial.begin( 115200 );
  Serial.println();
  Serial.println();

  #if MODO_MQTT==1
  // inicia conexión a la WiFi
  WiFi.setAutoConnect( true );
  WiFi.mode( WIFI_STA );
  WiFi.begin( WIFI_SSID, WIFI_PASS );

  // establece broker MQTT
  mqtt.setServer( MQTT_SERVER, MQTT_PORT );
  #endif

  // colocar aquí inicialización de sensores
  dht.begin();

  // requerido para dar tiempo a los sensores
  delay( 500 );
}

void loop()
{
  char str[32];
  StaticJsonBuffer<300> jsonBuffer;
  JsonObject& json = jsonBuffer.createObject();
  json["id"] = MQTT_CLIENTID;

  // Sensor DHT22
  float dhtTemperatura = dht.readTemperature();
  float dhtHumedad = dht.readHumidity();
  json["temperatura"] = double_with_n_digits( dhtTemperatura, 1 );
  json["humedad"] = double_with_n_digits( dhtHumedad, 1 );
  yield();

  Serial.print( "Temperatura: " );
  Serial.print( dhtTemperatura, 1 );
  Serial.print( " °C" );
  Serial.print( ", Humedad:" );
  Serial.print( dhtHumedad, 1 );
  Serial.println( " %" );
  yield();

  // La data en JSON a transmitir
  json.printTo( Serial );
  Serial.println();

  #if MODO_MQTT==0
  delay( MS_SLEEP );
  return;
  #endif

  // esperamos la conexión a la WiFi
  Serial.print( "Verificando WiFi ." );
  unsigned long start = millis();
  while( ( millis() - start ) < 15UL * 1000UL ){
    Serial.print( "." );
    if(  WiFi.status() == WL_CONNECTED ){
      Serial.println( " : Conectado." );

      // conectamos con el broker MQTT
      Serial.println ( "Conectando a servidor MQTT" );
      if( mqtt.connect( MQTT_CLIENTID.c_str() ) ){
        Serial.println( "Publicando ..." );

        // publicamos la data
        String payload;
        json.printTo( payload );
        mqtt.publish( MQTT_TOPIC, payload.c_str() );
      }
      break;
    } else {
      delay( 500 );
    }
  }

  Serial.println();
  Serial.println( "Reiniciando ..." );

  // repetimos el proceso con la pausa apropiada
  #if DEEP_SLEEP==0
  delay( MS_SLEEP );
  #else
  ESP.deepSleep( MS_SLEEP * 1000UL);
  #endif
}
