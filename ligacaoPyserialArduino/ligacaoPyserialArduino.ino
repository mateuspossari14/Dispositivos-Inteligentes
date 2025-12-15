#include "Ultrasonic.h"

#define Trig1 13
#define Trig2 11
#define Echo1 7
#define Echo2 12

#define velmotor 6
#define mla 4
#define mlb 5
#define velmotor2 10
#define mla2 9
#define mlb2 8
#define tmp 3000

#define ledVermelho A0
#define buzz A1
#define ledVerde A2

int vel = 125;

int time = 0;
int tempo1 = 0;
int tempo2 = 0;
int distancia1 = 0;
int distancia2 = 0;


bool autorizado = false;

HC_SR04 sensor1(13, 11);
HC_SR04 sensor2(12, 7);

void setup() {
  Serial.begin(9600);
  pinMode(velmotor, OUTPUT);
  pinMode(velmotor2, OUTPUT);
  pinMode(mla, OUTPUT);
  pinMode(mlb, OUTPUT);
  pinMode(mla2, OUTPUT);
  pinMode(mlb2, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(buzz, OUTPUT);


  digitalWrite(ledVermelho, LOW);

  digitalWrite(mla, LOW);
  digitalWrite(mlb, LOW);
  digitalWrite(mla2, LOW);
  digitalWrite(mlb2, LOW);
  analogWrite(velmotor, vel);
  analogWrite(velmotor2, vel);
  digitalWrite(ledVermelho, LOW);
  digitalWrite(ledVerde, HIGH);
  if (Serial.available() > 0) {
    digitalWrite(ledVerde, HIGH);
    delay(500);
    digitalWrite(ledVerde, LOW);
    delay(500);
    digitalWrite(ledVerde, HIGH);
    delay(500);
    digitalWrite(ledVerde, LOW);
    delay(500);
  }
}

void loop() {
  analogWrite(velmotor, vel);
  analogWrite(velmotor2, vel);

  
  if (Serial.available() > 0) {
    String dado = Serial.readStringUntil("\n");
    Serial.println(dado);
    if (dado == "1") {
      autorizado = true;
    } else {
      autorizado = false;
    }
  }

  if (autorizado) {
    Serial.print(sensor1.distance());
    Serial.print("       ");
    delay(100);
    Serial.println(sensor2.distance());
    
    if (sensor1.distance() > 10) {
      delay(500);
      if (sensor2.distance() > 10) {
        subir();
        delay(400);
        digitalWrite(mla, LOW);
        digitalWrite(mlb, LOW);
        digitalWrite(mla2, LOW);
        digitalWrite(mlb2, LOW);
        digitalWrite(buzz,LOW);
      }
    }

    delay(3000);
    if (sensor1.distance() > 14) {
      delay(500);
      if (sensor2.distance() > 14) {
        digitalWrite(buzz,LOW);
        digitalWrite(ledVermelho, LOW);
        digitalWrite(ledVerde, HIGH);
        descer();
        delay(400);
        digitalWrite(mla, LOW);
        digitalWrite(mlb, LOW);
        digitalWrite(mla2, LOW);
        digitalWrite(mlb2, LOW);
        delay(2000);
      }else{
        digitalWrite(mla, LOW);
        digitalWrite(mlb, LOW);
        digitalWrite(mla2, LOW);
        digitalWrite(mlb2, LOW);
        digitalWrite(ledVermelho, HIGH);
        digitalWrite(ledVerde, LOW);
        digitalWrite(buzz,HIGH);
      }
    } else {
      digitalWrite(mla, LOW);
      digitalWrite(mlb, LOW);
      digitalWrite(mla2, LOW);
      digitalWrite(mlb2, LOW);
      digitalWrite(ledVermelho, HIGH);
      digitalWrite(ledVerde, LOW);
      digitalWrite(buzz,HIGH);
    }

  } else {
    digitalWrite(ledVermelho, LOW);
    digitalWrite(ledVerde, LOW);
    digitalWrite(buzz,LOW);
  }

  // Serial.print(sensor1.distance());
  // Serial.print("       ");
  // delay(100);
  // Serial.println(sensor2.distance());

  // int distanciaUltrassonico1 = sensor1.distance();
  // int distanciaUltrassonico2 = sensor2.distance();

  // // if (distanciaUltrassonico1 > 0 && distanciaUltrassonico1 < 16 && distanciaUltrassonico2 < 17) {
  // //   digitalWrite(ledVermelho, HIGH);

  // // } else {
  // //   digitalWrite(ledVermelho, LOW);
  // // }

  // if (distanciaUltrassonico1 > 0 && distanciaUltrassonico1 < 16) {
  //   delay(200);
  //   if (distanciaUltrassonico2 < 17) {
  //     digitalWrite(ledVermelho, HIGH);
  //   }
  // } else {

  //     digitalWrite(ledVermelho, LOW);
  // }
}

void subir() {
  //Liga o motor A em uma direção
  digitalWrite(mla, LOW);
  digitalWrite(mlb, HIGH);
  digitalWrite(mla2, LOW);
  digitalWrite(mlb2, HIGH);
}

void descer() {
  digitalWrite(mla, HIGH);
  digitalWrite(mlb, LOW);
  digitalWrite(mla2, HIGH);
  digitalWrite(mlb2, LOW);
}
