import serial
import serial.tools.list_ports
import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# ======== AWS IoT CONFIG =========
CLIENT_ID = "arduino_iot_client"
TOPIC = "iot/roadquality/data"
CA_PATH = "AmazonRootCA1.pem"
CERT_PATH = "33079386daa68268fbdfb3a5775287957895b48855d2a6cb8139b0af5346b452-certificate.pem.crt"
KEY_PATH = "33079386daa68268fbdfb3a5775287957895b48855d2a6cb8139b0af5346b452-private.pem.key"
ENDPOINT = "a2lcpre30ozdfo-ats.iot.ap-south-1.amazonaws.com"   # <-- replace this with your AWS IoT endpoint
BAUD_RATE = 115200
# =================================

def find_arduino_port():
    """Auto-detect Arduino serial port."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if ("Arduino" in p.description) or ("usbserial" in p.device) or ("ttyUSB" in p.device) or ("ttyACM" in p.device):
            print(f"✅ Arduino detected on {p.device}")
            return p.device
    raise Exception("❌ No Arduino found. Plug it in and try again.")

def connect_aws():
    """Connect securely to AWS IoT Core."""
    mqtt = AWSIoTMQTTClient(CLIENT_ID)
    mqtt.configureEndpoint(ENDPOINT, 8883)
    mqtt.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)
    mqtt.configureOfflinePublishQueueing(-1)
    mqtt.configureDrainingFrequency(2)
    mqtt.configureConnectDisconnectTimeout(10)
    mqtt.configureMQTTOperationTimeout(5)
    mqtt.connect()
    print("✅ Connected to AWS IoT Core")
    return mqtt

def main():
    port = find_arduino_port()
    ser = serial.Serial(port, BAUD_RATE, timeout=2)
    mqtt = connect_aws()
    print("🚀 Streaming data from Arduino to AWS...\n")

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            # Expecting JSON lines from Arduino
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"⚠️ Skipped non-JSON line: {line}")
                continue

            mqtt.publish(TOPIC, json.dumps(data), 0)
            print(f"📤 Sent: {data}")

        except serial.SerialException:
            print("❌ Serial connection lost. Retrying...")
            time.sleep(2)
            port = find_arduino_port()
            ser = serial.Serial(port, BAUD_RATE, timeout=2)

        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")
            break

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}\n")






