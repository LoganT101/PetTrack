import serial
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# define Arduino serial
arduino_port = '/dev/ttyACM0'

# define GPIO pins for buzzer and LED
buzzer_pin = 7
led_pin = 8

# setup GPIO mode and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

# initialize PWM for buzzer
buzzer_pwm = GPIO.PWM(buzzer_pin, 1000)

# initialize LED to off
GPIO.output(led_pin, GPIO.LOW)

# MQTT Setup
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "motion_sensor"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message published")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(MQTT_HOST, MQTT_PORT, 60)

# open the serial with Arduino
ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)

try:
    while True:
        if ser.in_waiting > 0:
            # read line from serial 
            line = ser.readline().decode('utf-8').rstrip()
            print("Received from Arduino:", line)

            # split Arduino output into time and state
            time_and_state = line.split('-')
            state = time_and_state[1]

            if state == 'active':
                print("Motion detected. Turning on buzzer and LED.")
                buzzer_pwm.start(50)
                GPIO.output(led_pin, GPIO.HIGH)
                client.publish(MQTT_TOPIC, "Motion Detected!")
            else:
                print("No motion detected. Turning off buzzer and LED.")
                buzzer_pwm.stop()  # stop PWM to turn off buzzer
                GPIO.output(led_pin, GPIO.LOW)
                client.publish(MQTT_TOPIC, "No Motion")

except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()
    ser.close()
