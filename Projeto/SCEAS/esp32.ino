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

WebServer server(80);

// Definição de pinos
#define LED_ONBOARD 33  // LED onboard da ESP32-CAM
#define BUTTON_PIN 14  // Pino de um botão para controlar a leitura

// Resoluções da câmera
static auto loRes = esp32cam::Resolution::find(320, 240);
static auto midRes = esp32cam::Resolution::find(350, 530);
static auto hiRes = esp32cam::Resolution::find(800, 600);

// Função para capturar e servir imagens JPEG
void serveJpg() {
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));

  // Decodificar o QR Code se a leitura estiver habilitada
  String qrCodeData = decodeQRCode(frame);
  if (qrCodeData != "") {
    Serial.println("QR Code lido: " + qrCodeData);
    sendToFirebase(qrCodeData);
    digitalWrite(LED_ONBOARD, HIGH);  // Indicar sucesso com o LED
    delay(1000);
    digitalWrite(LED_ONBOARD, LOW);
  } else {
    Serial.println("Falha na leitura do QR Code");
    for (int i = 0; i < 3; i++) {  // Piscar o LED em caso de falha
      digitalWrite(LED_ONBOARD, HIGH);
      delay(300);
      digitalWrite(LED_ONBOARD, LOW);
      delay(300);
    }
  }

  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}

// Função para enviar o QR Code ao Firebase
void sendToFirebase(String qrData) {
  String path = "/leituraQR";

  // Enviar os dados ao Firebase
  if (Firebase.setString(firebaseData, path, qrData)) {
    Serial.println("Dados enviados ao Firebase com sucesso.");
  } else {
    Serial.println("Falha ao enviar ao Firebase: " + firebaseData.errorReason());
  }
}

// Função para decodificar QR Code
String decodeQRCode(std::unique_ptr<esp32cam::Frame>& frame) {
    // Corrigir!!!!
  return "";
}

// Função para inicializar a câmera
void initCamera() {
  using namespace esp32cam;
  Config cfg;
  cfg.setPins(pins::AiThinker);
  cfg.setResolution(hiRes);
  cfg.setBufferCount(2);
  cfg.setJpeg(80);

  bool ok = Camera.begin(cfg);
  Serial.println(ok ? "Câmera iniciada com sucesso" : "Falha ao iniciar a câmera");
}

// Função para configurar o Firebase
void initFirebase() {
  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;

  Firebase.begin(&config, &auth);

  // Tente conectar ao Firebase
  if (!Firebase.signUp(&config, &auth, USER_EMAIL, USER_PASSWORD)) {
    Serial.printf("Falha ao conectar ao Firebase: %s\n", config.signer.signupError.message.c_str());
  } else {
    Serial.println("Firebase conectado com sucesso!");
  }
  Firebase.reconnectWiFi(true);
}