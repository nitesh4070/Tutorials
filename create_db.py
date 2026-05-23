from influxdb import InfluxDBClient

client = InfluxDBClient(
    host='localhost',
    port=8086
)

client.create_database('vehicle_data')

print("Database Created Successfully")
