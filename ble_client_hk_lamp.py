import asyncio
from bleak import BleakClient, BleakScanner

# UUIDs must match the BLE server
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"  # Server Service UUID
CHARACTERISTIC_UUID = "abcd1234-5678-1234-5678-abcdef012345"  # Server Characteristic UUID

# ESP32_OnOff_BLE (40:91:51:99:E9:36)

async def send_command(client, command):
    if client.is_connected:
        await client.write_gatt_char(CHARACTERISTIC_UUID, command.encode("utf-8"))
        print(f"Sent: {command}")
    else:
        print("Failed to send: Not connected to server.")

async def run():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    # Display all discovered devices
    for i, device in enumerate(devices):
        print(f"{i}: {device.name} {device.metadata}")

    # Find a device advertising the desired service UUID
    target_device = None
    for device in devices:
        if SERVICE_UUID in [service for service in device.metadata.get("uuids", [])]:
            target_device = device
            break

    if not target_device:
        print("No device with the target service UUID found.")
        return

    print(f"Connecting to {target_device.name} ({target_device.address})...")
    async with BleakClient(target_device.address) as client:
        print("Connected to server. Type 'on' or 'off' to send commands.")
        while True:
            command = input("> ").strip()
            if command.lower() in ["on", "off"]:
                await send_command(client, command)
            elif command.lower() == "exit":
                print("Exiting...")
                break
            else:
                print("Unknown command. Use 'on', 'off', or 'exit'.")

# Run the asyncio event loop
asyncio.run(run())

