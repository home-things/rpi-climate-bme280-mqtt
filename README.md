# rpi-climate-bme280-mqtt
Temperature, Humidity, Pressure MQTT publisher

# Setup
`sudo vim /boot/config.txt`
```
dtparam=i2c_arm=on
dtparam=i2c0=off
dtparam=i2c1=on # BME280 Humidity sensor
```
pinout (gpio 2,3; 3v3; gnd)
```sh
sudo adduser pi i2c
sudo modprobe i2c-dev # source
pip3 install RPi.bme280
sudo apt-get install -y i2c-tools && i2cdetect -y 1 # Выясняем адрес
```

I took setup details from 2 sources:
- https://github.com/rm-hull/bme280
- I2C troubleshooting: https://www.raspberrypi.org/forums/viewtopic.php?t=115080

# Thanks 
Uses https://github.com/rm-hull/bme280 library
