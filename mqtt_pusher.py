import json, time
import smbus2, bme280
import paho.mqtt.client as mqtt

port = 1
address = 0x76
bus = smbus2.SMBus(port)

# Hey, If you don't want to fork it, let's create env variable config
MQTT_HOST = '192.168.1.68' 
MQTT_TOPIC = '/bedroom/weather/climate'
# https://www.home-assistant.io/integrations/sensor.mqtt/
# https://www.home-assistant.io/docs/mqtt/discovery#motion-detection-binary-sensor
#MQTT_CONF_TOPIC = 'homeassistant/sensor/bedroom/config'
#HA_MQTT_CONF = {
#        'name': "AirClimate Temperature Bedroom",
#        'state_topic': MQTT_TOPIC,
#        'unit_of_measurement': "C",
#        'value_template': "{{ value_json.temperature }}"
#}

print("[mqtt] initing...")
mqttc = mqtt.Client(client_id = MQTT_TOPIC, clean_session = False)

def pub_mqtt(jsonrow):
    #cmd = ['mosquitto_pub', '-h', MQTT_HOST, '-t', MQTT_TOPIC, '-s']
    #print('Publishing using:', cmd)
    #with subprocess.Popen(cmd, shell=False, bufsize=0, stdin=subprocess.PIPE).stdin as f:
    #    json.dump(jsonrow, f)
    payload = json.dumps(jsonrow)
    mqttc.publish(MQTT_TOPIC, payload, retain=True)
    print('>mqtt', payload)

def on_connect(mqttc, userdata, flags, rc):
    global is_mqtt_connected

    print("Connected to mqtt with result code "+str(rc))
    #print(f"[mqtt] subscribing... {MQTT_TOPIC_CMD}")
    #mqttc.subscribe(MQTT_TOPIC_CMD)
    #mqttc.subscribe(MQTT_TOPIC_SW_CMD)
    #print("[mqtt] subscribed")
    is_mqtt_connected = True

mqttc.enable_logger(logger=None)
mqttc.on_connect = on_connect
#mqttc.on_message = on_message
print("[mqtt] connecting...")
mqttc.connect(MQTT_HOST)

# mqttc.loop_forever()
mqttc.loop_start() # loop thread

if __name__ == "__main__":
    #print('auto conf ha mqtt sensor')
    #pub_mqtt(HA_MQTT_CONF)
    print("start bme280 loopback...")
    while True:
        calibration_params = bme280.load_calibration_params(bus, address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        data = bme280.sample(bus, address, calibration_params)

        # the compensated_reading class has the following attributes
        #print(data.id)
        #print(data.timestamp)
        #print(data.temperature)
        #print(data.pressure)
        #print(data.humidity)

        # there is a handy string representation too
        print(data)
        pub_mqtt({ 'temperature': "{0:.1f}".format(data.temperature), 'humidity': "{0:.1f}".format(data.humidity), 'pressure': "{0:.1f}".format(data.pressure) })

        print("Going to sleep for 1 min...")
        time.sleep(60)
