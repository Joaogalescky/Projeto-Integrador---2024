#include "ESPino32CAM.h"
#include "ESPino32CAM_QRCode.h"
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
const char* server_url = "http://<your_server_ip>:5000/upload";  // Endereço do servidor Python

ESPino32CAM cam;
ESPino32QRCode qr;

#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22
#define flash 4

int trava;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando-se ao WiFi...");
  }

  Serial.println("WiFi Conectado");
  Serial.println("Leitor de QR Code");

  pinMode(flash, OUTPUT);
  digitalWrite(flash, LOW); // Desliga o flash

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;
   
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Falha na inicialização da câmera com erro 0x%x", err);
    delay(1000);
    ESP.restart();
  }

  qr.init(&cam);
  sensor_t *s = cam.sensor();
  s->set_framesize(s, FRAMESIZE_CIF);
  s->set_whitebal(s, true);

  Serial.println("Aguardando código...");
}

void loop() {
  camera_fb_t *fb = cam.capture();
  if (!fb) {
    Serial.println("Falha na captura da imagem");
    return;
  }

  dl_matrix3du_t *rgb888, *rgb565;
  if (cam.jpg2rgb(fb, &rgb888)) {
    rgb565 = cam.rgb565(rgb888);
  }
  
  cam.clearMemory(rgb888);
  cam.clearMemory(rgb565);

  dl_matrix3du_t *image_rgb;
  if (cam.jpg2rgb(fb, &image_rgb)) {
    cam.clearMemory(fb);

    qrResoult res = qr.recognition(image_rgb);

    if (res.status) {
      if (trava == 0) {
        trava = 1;
        String leitura = "Código QR Lido: " + res.payload;
        Serial.println(leitura);
        
        // Enviar o QR Code para o servidor Python via HTTP POST
        HTTPClient http;
        http.begin(server_url);
        http.addHeader("Content-Type", "application/json");
        
        String jsonData = "{\"data\": \"" + res.payload + "\"}"; // Criar JSON a ser enviado
        int httpResponseCode = http.POST(jsonData);
        
        if (httpResponseCode > 0) {
          Serial.println("Dados enviados para o servidor com sucesso.");
        } else {
          Serial.println("Erro ao enviar dados para o servidor.");
        }
        http.end();
      }
    } else {
      trava = 0;
      Serial.println("Aguardando código...");
    }
  }

  cam.clearMemory(image_rgb);
}
