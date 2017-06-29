import time
import math
import vcgencmd
import os
import json
import requests

from datetime import datetime
from envirophat import light, weather, leds

hook = os.environ["SLACK_WEBHOOK"]

temp = 0
tempmed = 0
temp_calibrated = 0
cpu_temp = 0

factor = 1.11753815

out = open('enviro.log', 'w')
out.write('Time\tTemp (Sensor)\tTemp (Calibrated)\tTemp (Rounded)\tCPU Temp\n')


def send_message():
    payload = {'text':message}
    r = requests.post(hook, json=payload)

def get_temps():
    global cpu_temp
    cpu_temp = vcgencmd.measure_temp()
    global temp
    temp = weather.temperature()
    global temp_calibrated
    temp_calibrated = temp - ((cpu_temp - temp)/factor)
    global tempmed
    tempmed = '{:.1f}'.format(round(temp_calibrated, 2))

try:
    while True:
        leds.on()
        currtime = datetime.now().strftime('%H:%M:%S')
        lux = light.light()
        get_temps()
        out.write('%s\t%f\t%f\t%s\t%f\n' % (currtime, temp, temp_calibrated, tempmed, cpu_temp))
        message = "It is " + str(currtime) + "\nThe current temperature is " + str(tempmed) + " measuring " + str(lux) + " lux of light"
        send_message()
        out.flush()
        leds.off()
        time.sleep(30)

except KeyboardInterrupt:
    leds.off()
    out.close()
