/*
 * SMART HIDROPONIK
 * Sensor : pH 4502C, NTC 10K Thermistor, Analog TDS sensor
 * Display : LCD I2C GPIO21 & GPIO22, Streamlit Apps
 * Relay 4 Channel
*/

//inisiasi sensor pH
#define pHpin 32  //GPIO15
float pH, voltage;
int valX = 0;
const float pHA = 8.3;
const float pHB = 3.4;
float valAX = 534;
float valBX = 1580;
float slopeX, interceptX;

//inisiasi sensor TDS
#define TDSpin 33
float tds, valY;
const float tdsA =  693;
const float tdsB = 404;
float valAY = 85.00;
float valBY = 59.00;
float slopeY, interceptY;

//inisiasi sensor suhu ntc 10k
#define NTCpin 35
float suhu, valZ;
float R1 = 220000;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
float tempAcal = 40.2;
float tempBcal = 26.9;
float tempA = -94.32; //int valAZ = 10;
float tempB = -124.00; //int valBZ = 263;
float slopeZ, interceptZ;

//inisiasi lcd i2c
#include "Wire.h"
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd (0x27, 16, 2);

//inisiasi relay 4 channel
#define relay1 25
#define relay2 26
#define relay3 27
#define relay4 14

//inisiasi wifi
#include <WiFi.h>
const char* ssid = "enumatechz";
const char* password = "3numaTechn0l0gy";

//inisiasi waktu
#include <NTPClient.h>
#include <WiFiUdp.h>
String NTP;
const long utcOffsetInSeconds = 25200;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "id.pool.ntp.org", utcOffsetInSeconds);

// inisiasi streamlit
#include <HTTPClient.h>
#include <ArduinoJson.h>
const char* serverName = "http://192.168.1.2:5000/dapat_data";
unsigned long previousMillis = 0;
const long interval = 10000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  pinMode(pHpin,INPUT); //inisiasi sensor pH
  pinMode(TDSpin,INPUT); //inisiasi TDS
  pinMode(NTCpin,INPUT); //inisiasi suhu ntc 10k
  lcd.init(); lcd.backlight(); //inisiasi lcd
  lcd.setCursor(0, 0);  lcd.print("Hello Smart Hidroponik...");
  WiFi.begin(ssid, password); //inisiasi wifi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  timeClient.begin();//inisiasi waktu
}

 void loop(){
  timeNTP();
  pHmeter();
  TDSmeter();
  tempWater();
  Relay();
  Display();
  Streamlit();
 }

 void timeNTP() {
  timeClient.update();
  NTP = timeClient.getFormattedTime();
  delay(1000);
 }

 void pHmeter() {
  long sumX = 0;
  Serial.print("X = ");
  for (int i=0; i<10; i++) {
    valX = analogRead(pHpin);
    sumX += valX;
    Serial.print(valX);
    Serial.print(" ");
    delay(100);
  }
    Serial.println(" ");
    float averageX = sumX/10;
    slopeX = (pHA - pHB) / (valAX - valBX);
    interceptX = pHA - (slopeX * valAX);
    float voltageX = averageX*(3.3/4095.0);
    float pHX = (3.3*voltageX);
    pH = slopeX * pHX + interceptX;
}

void TDSmeter() {
  long sumY = 0;
  Serial.print("Y = ");
  for (int i=0; i<10; i++) {
    valY = analogRead(TDSpin);
    sumY += valY;
    Serial.print(valY);
    Serial.print(" ");
    delay(100);
  }
    Serial.println(" ");
    float averageY = sumY/10.0;
    slopeY = (tdsA - tdsB) / (valAY - valBY);
    interceptY = tdsA - (slopeY * valAY);
    tds = slopeY * averageY + interceptY;
    if (tds<0) {
      tds = 53.00;
    }
  }

void tempWater() {
  long sumZ = 0;
  Serial.print("Z = ");
  for (int i=0; i<10; i++) {
    valZ = analogRead(NTCpin);
    sumZ += valZ;
    Serial.print(valZ);
    Serial.print(" ");
    delay(100);
  }
  Serial.println(" ");
  float averageZ = sumZ/10;
  slopeZ = (tempAcal - tempBcal) / (tempA - tempB);
  interceptZ = tempAcal - (slopeZ * tempA);
  R2 = R1 * (4095.0 / (float)averageZ - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2)) - 273.15;
  suhu = slopeZ * T + interceptZ;
}

void Relay () {
   // Mengatur relay berdasarkan nilai pH
  if (pH >= 0 && pH < 5.0) {          //Jika terlalu asam, maka pH dinaikkan dengan menambahkan basa
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, HIGH);
  } else if (pH > 6.0 && pH <= 14.0) {  //Jika terlalu basa, maka pH diturunkan dengan menambahkan asam
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, LOW);
  } else {                              //kondisi normal, relay 1 dan relay 2 untuk asam-basa mati
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
  }
  // Mengatur relay berdasarkan nilai TDS
  if (tds >= 0 && tds <= 1100) {         //Jika nilai tds rendah (< 400 ppm), maka ditambahkan Nutrisi
    digitalWrite(relay3, LOW);
  } else {                              //kondisi normal, relay 3 mati untuk pupuk
    digitalWrite(relay3, HIGH);
  }
    // Mengatur relay berdasarkan nilai suhu
  if (suhu >= 26 && suhu <= 100) {     //Jika terlalu panas, maka diturunkan suhunya dengan kipas
    digitalWrite(relay4, LOW);
  } else {                            //kondisi normal, relay 4 mati untuk suhu/kipas
    digitalWrite(relay4, HIGH);
  }
}

void Display () {
  Serial.println("_SMART HIDROPONIK_");
  Serial.print(NTP); Serial.print('\t');
  Serial.print("pH = "); Serial.print(pH); Serial.print('\t');
  Serial.print("TDS = "); Serial.print(tds); Serial.print(" ppm"); Serial.print('\t');
  Serial.print("suhu = "); Serial.print(suhu); Serial.println(" C"); 
  Serial.println("");
  //lcd
  lcd.clear();
  lcd.setCursor(0, 0);  lcd.print(NTP);
  lcd.setCursor(0, 1);  lcd.print(" ");    lcd.print(pH);
  lcd.setCursor(4, 1);  lcd.print(" ");    lcd.print(tds);
  lcd.setCursor(9, 1);  lcd.print(" ");    lcd.print(suhu);
  }

void Streamlit() { //streamlit
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
        if ((WiFi.status() == WL_CONNECTED)) {
          HTTPClient http;
          http.begin(serverName);
          http.addHeader("Content-Type", "application/json");
          StaticJsonDocument<200> jsonDoc;
            jsonDoc["pH"] = round(pH * 100.0) / 100.0;
            jsonDoc["tds"] = round(tds * 100.0) / 100.0;
            jsonDoc["suhu"] = round(suhu * 100.0) / 100.0;

        // pengubah JSON menjadi string
        String httpRequestData;
        serializeJson(jsonDoc, httpRequestData);

        //  mengirimkan POST request
        int httpResponseCode = http.POST(httpRequestData);
        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(response);
        } else {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }
        http.end();
  }
  }
}
