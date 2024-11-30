#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0" // Random UUID
#define CHARACTERISTIC_UUID "abcd1234-5678-1234-5678-abcdef012345" // Random UUID

static const int RELAY_ENABLE = 13;

class MyCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        String value = pCharacteristic->getValue();
        if (value == "On") {
            Serial.println("Received: On");
            digitalWrite(RELAY_ENABLE, HIGH);
        } else if (value == "Off") {
            Serial.println("Received: Off");
            digitalWrite(RELAY_ENABLE, LOW);
        } else {
            Serial.println("Unknown command received: " + String(value.c_str()));
        }
    }
};

class ServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        Serial.println("Device connected.");
    }

    void onDisconnect(BLEServer* pServer) {
        Serial.println("Device disconnected. Restarting advertising...");
        pServer->getAdvertising()->start(); // Restart advertising to make the server visible again
    }
};

void setup() {
    Serial.begin(115200);
    pinMode(RELAY_ENABLE, OUTPUT);

    BLEDevice::init("HKHALID_WHITE_LAMP_BLE");
    BLEServer *pServer = BLEDevice::createServer();
    pServer->setCallbacks(new ServerCallbacks()); // Set server callbacks

    BLEService *pService = pServer->createService(SERVICE_UUID);

    BLECharacteristic *pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
        BLECharacteristic::PROPERTY_WRITE
    );

    pCharacteristic->setCallbacks(new MyCallbacks());

    pService->start();

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID); // Explicitly add the service UUID
    pAdvertising->setScanResponse(true);       // Include additional advertising data
    pAdvertising->start();

    Serial.println("BLE Service is ready. Waiting for connections...");
}

void loop() {
    // Keep BLE running
}
