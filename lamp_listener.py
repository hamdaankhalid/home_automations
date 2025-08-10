import asyncio
from bleak import BleakClient, BleakScanner
import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

# UUIDs must match the BLE server
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"  # Server Service UUID
CHARACTERISTIC_UUID = "abcd1234-5678-1234-5678-abcdef012345"  # Server Characteristic UUID

# ESP32_OnOff_BLE (40:91:51:99:E9:36)

addr = "40:91:51:99:E9:36"

async def send_command_with_reconnect(command):
    async with BleakClient(addr) as client:
        await client.write_gatt_char(CHARACTERISTIC_UUID, command.encode("utf-8"))
        print(f"Sent: {command}")
    
async def run():
    while True:
        with mic as source:
            print("Listening for command...")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="en-US").lower()
                if "wake up" in text:
                    print("wake up detected")
                    try:
                        await send_command_with_reconnect("On")
                    except Exception as e:
                        print(f"Error sending command: {e}")
                elif "go to sleep" in text:
                    print("sleep detected")
                    try:
                        await send_command_with_reconnect("Off")
                    except Exception as e:
                        print(f"Error sending command: {e}")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(run())

