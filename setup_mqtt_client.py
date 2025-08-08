#!/usr/bin/env python3
"""
Setup script for MQTT Gateway Client
This script helps you set up and run the MQTT client with the xiaozhi-esp32-server mqtt-gateway
"""

import os
import sys
import subprocess
import json

def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        'paho-mqtt',
        'pyaudio', 
        'keyboard',
        'cryptography',
        'opuslib',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_mqtt_gateway_config():
    """Check if mqtt-gateway is properly configured."""
    config_path = "main/mqtt-gateway/config/mqtt.json"
    
    if not os.path.exists(config_path):
        print(f"❌ MQTT Gateway config not found at: {config_path}")
        print("📝 Creating sample config...")
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Create sample config
        sample_config = {
            "debug": True,
            "development": {
                "mac_addresss": ["00_16_3e_fa_3d_de"],
                "chat_servers": ["ws://192.168.1.6:8000/xiaozhi/v1/"]
            },
            "production": {
                "chat_servers": ["ws://192.168.1.6:8000/xiaozhi/v1/"]
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(sample_config, f, indent=4)
        
        print(f"✅ Created sample config at: {config_path}")
        print("⚠️  Please update the chat_servers URL with your actual xiaozhi-server address")
        return False
    
    print("✅ MQTT Gateway config found")
    return True

def check_xiaozhi_server():
    """Check if xiaozhi-server is running."""
    import requests
    try:
        response = requests.get("http://192.168.1.6:8000", timeout=3)
        print("✅ xiaozhi-server appears to be running")
        return True
    except:
        print("❌ Cannot connect to xiaozhi-server at http://192.168.1.6:8000")
        print("   Make sure xiaozhi-server is running first")
        return False

def start_mqtt_gateway():
    """Start the MQTT gateway if it's not running."""
    gateway_path = "main/mqtt-gateway"
    
    if not os.path.exists(gateway_path):
        print(f"❌ MQTT Gateway not found at: {gateway_path}")
        return False
    
    print("🚀 Starting MQTT Gateway...")
    print("   (This will run in the background)")
    
    # Set environment variables
    env = os.environ.copy()
    env['MQTT_PORT'] = '1883'
    env['UDP_PORT'] = '8884'
    env['PUBLIC_IP'] = '192.168.1.6'
    
    try:
        # Start the gateway in the background
        process = subprocess.Popen(
            ['node', 'app.js'],
            cwd=gateway_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give it a moment to start
        import time
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ MQTT Gateway started successfully")
            print(f"   Process ID: {process.pid}")
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ MQTT Gateway failed to start")
            print(f"   Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start MQTT Gateway: {e}")
        return False

def main():
    print("🔧 Setting up MQTT Gateway Client for xiaozhi-esp32-server")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check xiaozhi-server
    if not check_xiaozhi_server():
        print("\n📋 To start xiaozhi-server:")
        print("   cd main/xiaozhi-server")
        print("   python app.py")
        return False
    
    # Check gateway config
    if not check_mqtt_gateway_config():
        return False
    
    print("\n🎯 Setup complete! You can now:")
    print("1. Start the MQTT Gateway:")
    print("   cd main/mqtt-gateway")
    print("   node app.js")
    print("\n2. Run the Python client:")
    print("   python client5.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)