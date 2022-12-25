import ssd1306
from machine import Pin, I2C
import network
import time 
from time import sleep
from machine import Pin,PWM
import dht
import ujson
from umqtt.simple import MQTTClient

# ------------------------------MQTT Server Parameters -----------------------

MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "wokwi-weather"

sensor = dht.DHT22(Pin(15))
p4 = machine.Pin(35)
freq=50
servo = machine.PWM(p4,freq)
frequency = 5000
led = PWM(Pin(13), frequency)


print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

# ---------------------------oled code----------------------------------

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def clear_oled():
  oled.fill(0)
  oled.show()

def show_oled(temp,humt,mes):
  clear_oled()
  oled.text("Temp :",10,10)
  oled.text(temp,60,10)
  oled.text("Humidity :",10,30)
  oled.text(humt,90,30)
  oled.text(mes,10,50)
  oled.show()



#----------------------------Main-------------------------------------
prev_temp = 0
prev_humt = 0
prev_weather = " "
while True:
  print("Measuring weather conditions... ", end="")
  sensor.measure() 
  temp = sensor.temperature(),
  humt = sensor.humidity(),
  if temp != prev_temp or humt != prev_humt :
    print("Updated!")
    if temp[0] > 40 :
      mes = "Switch on AC"
    elif temp[0] < 25 :
      mes = "switch on Heater"
    else :
      mes = ""
    print("Temp : ",temp)
    print("Humidity : ",humt)
    show_oled(str(temp[0]),str(humt[0]),mes)
    prev_temp = temp
    prev_humt = humt
  else:
    print("No change")
  time.sleep(1)
