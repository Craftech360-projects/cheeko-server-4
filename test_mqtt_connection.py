#!/usr/bin/env python3
"""
Simple MQTT connection test
"""
import paho.mqtt.client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion
import time
import json

# Configuration
MQTT_BROKER_HOST = "192.168.1.6"
MQTT_BROKER_PORT = 1883

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Successfully connected to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        client.subscribe("test/topic")
    else:
        print(f"❌ Failed to connect to MQTT broker. Return code: {rc}")

def on_message(client, userdata, msg):
    print(f"📨 Received message: {msg.topic} -> {msg.payload.decode()}")

def test_mqtt_connection():
    print(f"🔍 Testing MQTT connection to {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
    
    client = mqtt_client.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id="test_client_123"
    )
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        print("🔄 Attempting to connect...")
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        client.loop_start()
        
        # Wait a bit to see if connection succeeds
        time.sleep(3)
        
        # Try to publish a test message
        print("📤 Publishing test message...")
        client.publish("test/topic", "Hello from test client!")
        
        # Wait for any responses
        time.sleep(2)
        
        client.loop_stop()
        client.disconnect()
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_mqtt_connection()