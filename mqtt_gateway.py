import can
import json
import paho.mqtt.client as mqtt

# --------------------------------
# MQTT Configuration
# --------------------------------
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("MQTT Connected")

# --------------------------------
# CAN Interface
# --------------------------------
bus = can.Bus(
    channel='can0',
    interface='socketcan'
)

print("CAN Interface Ready")
print("Waiting for CAN Messages...\n")

# --------------------------------
# Main Loop
# --------------------------------
while True:

    message = bus.recv()

    can_id = message.arbitration_id
    data = list(message.data)

    # --------------------------------
    # Traffic Sign ECU
    # --------------------------------
    if can_id == 0x100:

        speed_limit = data[0]

        payload = {
            "speed_limit": speed_limit
        }

        mqtt_client.publish(
            "vehicle/traffic_sign",
            json.dumps(payload)
        )

        print("Published Traffic Sign")
        print(payload)

    # --------------------------------
    # AEB ECU
    # --------------------------------
    elif can_id == 0x200:

        aeb_state = data[0]

        if aeb_state == 0:
            state = "SAFE"

        elif aeb_state == 1:
            state = "WARNING"

        elif aeb_state == 2:
            state = "BRAKING"

        else:
            state = "UNKNOWN"

        payload = {
            "aeb_state": state
        }

        mqtt_client.publish(
            "vehicle/aeb",
            json.dumps(payload)
        )

        print("Published AEB Status")
        print(payload)