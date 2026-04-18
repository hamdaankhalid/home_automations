import asyncio
from bleak import BleakClient, BleakScanner

# UUIDs must match the BLE server
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"  # Server Service UUID
CHARACTERISTIC_UUID = "abcd1234-5678-1234-5678-abcdef012345"  # Server Characteristic UUID

# ESP32 BLE Device Address
DEVICE_ADDRESS = "40:91:51:99:E9:36"

async def explore_device(client):
    """Explore and print all services and characteristics of the connected device."""
    print("\n=== Device Services and Characteristics ===")
    for service in client.services:
        print(f"\nService: {service.uuid}")
        print(f"  Description: {service.description}")
        
        for char in service.characteristics:
            print(f"  Characteristic: {char.uuid}")
            print(f"    Properties: {char.properties}")
            print(f"    Description: {char.description}")
    print("===========================================\n")

async def send_command(client, command):
    if client.is_connected:
        await client.write_gatt_char(CHARACTERISTIC_UUID, command.encode("utf-8"))
        print(f"Sent: {command}")
    else:
        print("Failed to send: Not connected to server.")

async def run():
    print("Scanning for BLE devices...")
    devices_and_adv = await BleakScanner.discover(return_adv=True)
    
    print(f"Found {len(devices_and_adv)} devices")
    
    # Find a device advertising the desired service UUID
    target_device = None
    for device, adv_data in devices_and_adv.values():
        # Check if device advertises our service UUID
        advertised_uuids = adv_data.service_uuids
        print(f"Device: {device.name or 'Unknown'} ({device.address}) - UUIDs: {advertised_uuids}")
        
        if SERVICE_UUID in advertised_uuids:
            target_device = device
            print(f"✓ Found target device: {device.name} ({device.address})")
            break
    
    if not target_device:
        print(f"\nNo device advertising service UUID {SERVICE_UUID} found.")
        print("Trying direct connection to known address as fallback...")
        target_address = DEVICE_ADDRESS
    else:
        target_address = target_device.address
    
    print(f"\nConnecting to {target_address}...")
    
    async with BleakClient(target_address) as client:
        print("Connected to server.")
        
        # Explore device services and characteristics
        await explore_device(client)
        
        print("Type 'on' or 'off' to send commands.")
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

