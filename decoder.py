import can

print("Starting TCU Decoder...")

# Create CAN Bus Interface
bus = can.Bus(
    channel='can0',
    interface='socketcan'
)

print("CAN Interface Ready...")
print("Waiting for CAN messages...\n")

while True:

    message = bus.recv()

    can_id = message.arbitration_id
    data = list(message.data)

    # -----------------------------
    # Traffic Sign ECU
    # -----------------------------
    if can_id == 0x100:

        speed_limit = data[0]

        print("================================")
        print("Traffic Sign ECU Message")
        print(f"CAN ID      : {hex(can_id)}")
        print(f"Speed Limit : {speed_limit} km/h")
        print("================================\n")

    # -----------------------------
    # AEB ECU
    # -----------------------------
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

        print("================================")
        print("AEB ECU Message")
        print(f"CAN ID    : {hex(can_id)}")
        print(f"AEB State : {state}")
        print("================================\n")

    else:

        print("Unknown CAN Message")
        print(hex(can_id), data)