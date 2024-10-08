import json
import paho.mqtt.client as mqtt
import folium
import time
from folium.plugins import MarkerCluster

# Variable to hold the current latitude and longitude
latitude = 50.780036278929614
longitude = 6.10363592985153

# Callback function when a message is received
def on_message(client, userdata, message):
    global latitude, longitude
    # Convert the message payload from bytes to string
    data = message.payload.decode()
    # parse the json string
    data = json.loads(data)
    # Extract the latitude and longitude
    if 'GPS' in data:
        gps_data = data["GPS"]
        latitude = gps_data["Latitude"]
        longitude = gps_data["Longitude"]

# Create MQTT client
client = mqtt.Client()

# Attach callback function to the message event
client.on_message = on_message

# Connect to the MQTT broker
client.connect("broker.mqttdashboard.com", 1883)

# Subscribe to the desired topic
client.subscribe("gpsdata")

# Start the MQTT loop
client.loop_start()

# Initialize the map
# Initialize the map
m = folium.Map(location=[latitude, longitude], zoom_start=15)

mc = folium.MarkerCluster()
m.add_child(mc)

marker = None
while True:
    # Check if the latitude and longitude have been updated
    if latitude and longitude:
        # Remove the previous marker
        if marker:
            mc.remove_child(marker)
        # Update the marker on the map to the current location
        marker = folium.Marker(location=[latitude, longitude])
        mc.add_child(marker)

        # Save the map
        m.save("current_location.html")
    # Wait for one second
    time.sleep(1)
