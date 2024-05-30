#include "RTCZero.h"

RTCZero clock;

int sensor_pin = 2; // change to your data pin

void setup() {
  Serial.begin(9600);
  pinMode(sensor_pin, INPUT);

  clock.begin();
}

void loop() {
  Serial.print(clock.getHours());
  Serial.print(":");
  Serial.print(clock.getMinutes());
  Serial.print(":");
  Serial.print(clock.getSeconds());
  Serial.print("-");
  if (digitalRead(2) == HIGH) {
    Serial.println("active");
  }
  else {
    Serial.println("inactive");
  }
  delay(1000);
}
