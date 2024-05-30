import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from collections import deque
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# MQTT settings
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "motion_sensor"

# global variables
last_activity = "No activity"
last_timestamp = ""
sensor_state = "Inactive"
activity_log = deque(maxlen=5)  # maximum 5 instances of active activity
activity_times = []
activity_values = []

# MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global last_activity, last_timestamp, sensor_state
    print(msg.topic+" "+str(msg.payload))
    activity = msg.payload.decode()
    last_activity = "Motion Detected" if activity == "Motion Detected!" else "No Motion"
    last_timestamp = time.strftime("%H:%M:%S")
    sensor_state = "Active" if activity == "Motion Detected!" else "Inactive"
    update_interface()

def update_interface():
    # update labels
    current_state_label.config(text=f"Current Sensor State: {sensor_state}")
    if sensor_state == "Active":
        last_activity_label.config(text=f"Last Activity: {last_activity} at {last_timestamp}")
    
    # update activity log
    if sensor_state == "Active":
        activity_log.append(f"{last_activity} at {last_timestamp}")
    activity_log_text.set("\n".join(activity_log))

    # update graph
    activity_times.append(last_timestamp)
    activity_values.append(1 if sensor_state == "Active" else 0)
    ax.clear()
    ax.plot(activity_times, activity_values, marker='o')
    ax.set_title('Sensor Activity')
    ax.set_xlabel('Time')
    ax.set_ylabel('Activity')
    canvas.draw()

# MQTT Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# tkinter Setup
root = tk.Tk()
root.title("Motion Sensor Interface")

# labels
current_state_label = tk.Label(root, text=f"Current Sensor State: {sensor_state}", font=("Arial", 14))
current_state_label.pack(pady=10)

last_activity_label = tk.Label(root, text=f"Last Activity: {last_activity} at {last_timestamp}", font=("Arial", 12))
last_activity_label.pack(pady=10)

# activity log
activity_log_text = tk.StringVar()
activity_log_text.set("\n".join(activity_log))
activity_log_label = tk.Label(root, text="Activity Log", font=("Arial", 12))
activity_log_label.pack(pady=10)
activity_log_display = tk.Label(root, textvariable=activity_log_text, font=("Arial", 10))
activity_log_display.pack(pady=10)

# graph
fig, ax = plt.subplots(figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=10)

# start MQTT loop
client.loop_start()

# start tkinter loop
root.mainloop()
