// Bibliotecas
#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>
#include <FirebaseESP32.h>
#include <Arduino.h>

// Configurações de Wi-Fi
const char* WIFI_SSID = "ALHN-BA05";
const char* WIFI_PASS = "7740976294";

// Configurações do Firebase
#define API_KEY "AIzaSyAm4JouCBP2uqzbdgERpx_Jc8mSOEMooOU"
#define USER_EMAIL "joaocvgalescky@gmail.com"
#define USER_PASSWORD "sceas2024"
#define DATABASE_URL "https://sceas-49731.firebaseio.com"

// Objetos do Firebase
FirebaseData firebaseData;
FirebaseAuth auth;
FirebaseConfig config;