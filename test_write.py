from influxdb import InfluxDBClient

client = InfluxDBClient(
    host='localhost',
    port=8086
)

client.switch_database('vehicle_data')

json_body = [
    {
        "measurement": "traffic_sign",

        "fields": {
            "speed_limit": 80
        }
    }
]

client.write_points(json_body)

print("Test Data Written")
