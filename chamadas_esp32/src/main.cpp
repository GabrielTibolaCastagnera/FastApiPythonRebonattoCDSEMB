/*
Engenharia de Computação - UPF
Comunicação de dados em Aplicações Embarcadas
Gabriel Tibola Castagnera e Adrian Luithardt Klitzke
29/10/2023
Trabalho API REST em Python com chamadas na ESP32
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define DELAY_BETWEEN 2000
#define DELAY_BETWEEN_CYCLES 10000
#define PINO 34

const char *ssid = "Vanini";
const char *passwd = "Capital_das_olarias";

unsigned long lastTime = 0;

// Your Domain name with URL path or IP address with path
// Inserção do URI (URL + URN) a acessar
String uri = "http://192.168.0.5:8000/";

void acessaGET(String URN);
void acessaPOST(String URN, String body);
void acessaPUT(String URN, String body);
void acessaPatch(String URN);
void testarMetodos();
void printJson(String json);
void testarPost();
void testarPut();

void setup()
{
    Serial.begin(9600);
    delay(1000);
    Serial.println();
    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);
    // WiFi.begin(ssid);
    WiFi.begin(ssid, passwd);

    // WiFi.begin(ssid, WPA2_AUTH_PEAP, EAP_ANONYMOUS_IDENTITY, EAP_IDENTITY, EAP_PASSWORD); //WITHOUT CERTIFICATE - WORKING WITH EXCEPTION ON RADIUS SERVER

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("MAC address: ");
    Serial.println(WiFi.macAddress());
    Serial.println("");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    pinMode(GPIO_NUM_25, INPUT);
}

void loop()
{
    if ((millis() - lastTime) > DELAY_BETWEEN_CYCLES)
    {
        if (WiFi.status() == WL_CONNECTED)
        {
            testarMetodos();
        }
        else
        {
            Serial.println("WiFi Disconnected");
        }
        lastTime = millis();
    }
}

void testarMetodos()
{
    // insere 3 Dados Novos
    testarPost();
    Serial.print("LUZ: ");
    Serial.println(analogRead(34));
    // consulta o segundo dado inserido
    acessaGET("consultarEstufa?id=1");
    delay(DELAY_BETWEEN);
    // atualiza o segundo dado inserido
    testarPut();
    // consulta o segundo dado inserido
    acessaGET("consultarEstufa?id=1");
    delay(DELAY_BETWEEN);
    // consulta todos os dados
    acessaGET("consultarEstufa");
    delay(DELAY_BETWEEN);
    // exclui o segundo dado inserido
    acessaPatch("excluirEstufa?estufa_id=1");
    delay(DELAY_BETWEEN);
    // consulta todos os dados
    acessaGET("consultarEstufa");
    delay(DELAY_BETWEEN);
}

void testarPost()
{
    DynamicJsonDocument doc(1024);
    String serializedDoc;
    doc["id"] = 0;
    doc["nome"] = "estufa 1";
    doc["humidadeDoAr"] = 0.9;
    doc["humidadeDoSolo"] = 0.8;
    doc["qtdDeMudas"] = 130;
    doc["luminosidade"] = analogRead(PINO);
    serializeJson(doc, serializedDoc);
    acessaPOST("criarNovaEstufa", serializedDoc);
    delay(DELAY_BETWEEN);
    doc["id"] = 1;
    doc["luminosidade"] = analogRead(PINO);
    doc["nome"] = "Estufa 2";
    serializedDoc = "";
    serializeJson(doc, serializedDoc);
    acessaPOST("criarNovaEstufa", serializedDoc);
    delay(DELAY_BETWEEN);
    doc["id"] = 2;
    doc["luminosidade"] = analogRead(PINO);
    doc["nome"] = "Estufa 3";
    serializedDoc = "";
    serializeJson(doc, serializedDoc);
    acessaPOST("criarNovaEstufa", serializedDoc);
    delay(DELAY_BETWEEN);
}

void acessaGET(String URN = "")
{
    HTTPClient http;
    String rota;

    // Configura a conexão com URI via http
    rota = uri.c_str();
    rota.concat(URN.c_str());
    http.begin(rota.c_str());

    // Envia uma requisição com o método GET
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0)
    {
        String payload = "";
        Serial.print("Código de resposta GET: ");
        Serial.println(httpResponseCode);
        if (httpResponseCode == 200)
        {
            Serial.print("Retorno GET de ");
            Serial.println(rota.c_str());
            payload = http.getString();
        }
        else
        {
            payload = http.getString(); // Para evitar erros na biblioteca
            Serial.print("Erro no processamento da requisição ");
            Serial.println(rota.c_str());
        }
        printJson(payload);
    }
    else
    {
        Serial.print("Erro de acesso ao Serviço: ");
        Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
}

void testarPut()
{
    DynamicJsonDocument doc(1024);
    String serializedDoc;
    doc["id"] = 1;
    doc["nome"] = "estufa atualizada";
    doc["humidadeDoAr"] = 0.6;
    doc["luminosidade"] = analogRead(PINO);
    doc["humidadeDoSolo"] = 0.9;
    serializeJson(doc, serializedDoc);
    acessaPUT("atualizarEstufa", serializedDoc);
    delay(DELAY_BETWEEN);
}

void acessaPatch(String URN)
{
    HTTPClient http;
    String rota;

    // Configura a conexão com URI via http
    rota = uri.c_str();
    rota.concat(URN.c_str());
    http.begin(rota.c_str());

    // http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Envia uma requisição com o método GET
    int httpResponseCode = http.PATCH("");

    if (httpResponseCode > 0)
    {
        Serial.print("Código de resposta PATCH: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        printJson(payload);
    }
    else
    {
        Serial.print("Erro de acesso ao Serviço PATCH: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        printJson(payload);
    }
    // Free resources
    http.end();
}

void acessaPUT(String URN, String body = "")
{
    HTTPClient http;
    String rota;

    // Configura a conexão com URI via http
    rota = uri.c_str();
    rota.concat(URN.c_str());
    http.begin(rota.c_str());

    // http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Envia uma requisição com o método PUT
    int httpResponseCode = http.PUT(body);

    if (httpResponseCode > 0)
    {
        Serial.print("Código de resposta HTTP: ");
        Serial.println(httpResponseCode);
        if (httpResponseCode == 200)
        {
            Serial.print("Sucesso PUT de ");
            Serial.println(rota.c_str());
            String payload = http.getString();
            printJson(payload);
        }
        else
        {
            Serial.print("Erro no processamento da requisição PUT: ");
            Serial.println(httpResponseCode);
            String payload = http.getString();
            printJson(payload);
        }
    }
    else
    {
        Serial.print("Erro de acesso ao Serviço: ");
        Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
}

void acessaPOST(String URN, String body = "")
{
    HTTPClient http;
    String rota;

    // Configura a conexão com URI via http
    rota = uri.c_str();
    rota.concat(URN.c_str());
    http.begin(rota.c_str());

    // http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = http.POST(body);

    if (httpResponseCode > 0)
    {
        Serial.print("Código de resposta POST: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        printJson(payload);
    }
    else
    {
        Serial.print("Erro de acesso ao Serviço POST: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        printJson(payload);
    }

    // Free resources
    http.end();
}

void printJson(String json)
{
    DynamicJsonDocument jsonBuffer(1024);
    const char *a = json.c_str();
    DeserializationError error = deserializeJson(jsonBuffer, a);
    if (error)
    {
        Serial.println(F("deserializeJson() failed: "));
        Serial.println(error.c_str());
        return;
    }
    serializeJsonPretty(jsonBuffer, Serial);
    Serial.println("");
}
