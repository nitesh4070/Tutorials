from flask import Flask, render_template_string
import paho.mqtt.client as mqtt
import json
import threading

app = Flask(__name__)

# -----------------------------
# Global Vehicle State
# -----------------------------
vehicle_data = {
    "speed_limit": "--",
    "aeb_state": "--"
}

# -----------------------------
# MQTT Callback
# -----------------------------
def on_message(client, userdata, msg):

    topic = msg.topic
    payload = json.loads(msg.payload.decode())

    if topic == "vehicle/traffic_sign":
        vehicle_data["speed_limit"] = payload["speed_limit"]

    elif topic == "vehicle/aeb":
        vehicle_data["aeb_state"] = payload["aeb_state"]

# -----------------------------
# MQTT Setup
# -----------------------------
mqtt_client = mqtt.Client()

mqtt_client.on_message = on_message

mqtt_client.connect("localhost", 1883, 60)

mqtt_client.subscribe("vehicle/#")

# MQTT loop in background thread
threading.Thread(
    target=mqtt_client.loop_forever,
    daemon=True
).start()

# -----------------------------
# Dashboard UI
# -----------------------------
HTML = """
<!DOCTYPE html>
<html>

<head>
    <title>SDV Dashboard</title>

    <meta http-equiv="refresh" content="1">

    <style>
        body {
            font-family: Arial;
            background-color: #111;
            color: white;
            padding: 30px;
        }

        .card {
            background: #222;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            width: 300px;
        }

        h1 {
            color: cyan;
        }

        .value {
            font-size: 40px;
            color: lime;
        }
    </style>
</head>

<body>

    <h1>SDV Local Dashboard</h1>

    <div class="card">
        <h2>Traffic Sign Speed Limit</h2>
        <div class="value">
            {{speed_limit}} km/h
        </div>
    </div>

    <div class="card">
        <h2>AEB State</h2>
        <div class="value">
            {{aeb_state}}
        </div>
    </div>

</body>
</html>
"""

# -----------------------------
# Flask Route
# -----------------------------
@app.route("/")
def dashboard():

    return render_template_string(
        HTML,
        speed_limit=vehicle_data["speed_limit"],
        aeb_state=vehicle_data["aeb_state"]
    )

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
