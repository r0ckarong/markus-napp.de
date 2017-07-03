import time
import math
import vcgencmd
import os
import json
import requests

from datetime import datetime
from envirophat import light, weather, leds

temp = 0
tempmed = 0
temp_calibrated = 0
cpu_temp = 0
outside_temp = 0
outside_location = ""
outside_condition = ""
currtime = datetime.now().strftime('%H:%M:%S')

slack_webhook = os.environ["SLACK_WEBHOOK"]

# Data for Openweathermap Query
owm_key = os.environ["OWM_KEY"]
zip_code = "60433"
country_code = "de"
unit = "metric"

# Sensor offset factor
factor = 0.868218182

out = open('enviro.log', 'w')
out.write('Time\tTemp (Sensor)\tTemp (Calibrated)\tTemp (Rounded)\tCPU Temp\n')

def get_outside():
    global outside_temp
    global outside_condition
    global outside_location

    owm_api = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip_code + "," + country_code + "&units=" + unit + "&appid=" + owm_key

    outside = json.loads(requests.get(owm_api).text)
    outside_temp = outside['main']['temp']
    outside_condition = outside['weather'][0]['description']
    outside_location = outside['name']

def get_temps():
    global cpu_temp
    global temp
    global tempmed
    global temp_calibrated

    cpu_temp = vcgencmd.measure_temp()

    temp = weather.temperature()
    temp_calibrated = temp - ((cpu_temp - temp)/factor)
    tempmed = '{:.1f}'.format(round(temp_calibrated, 2))

def send_message():
    mytime = str(currtime)
    out_temp = str(outside_temp)
    med = str(tempmed)

    post = """It is currently %s in %s, %s
    Outside there is %s at %s C
    Inside the office we have a temperature of %s C
    """

    message = post % (mytime, zip_code, outside_location, outside_condition, out_temp, med)

    payload = {'text':message}
    requests.post(slack_webhook, json=payload)

def write_file():
    out.write('%s\t%f\t%f\t%s\t%f\n' % (currtime, temp, temp_calibrated, tempmed, cpu_temp))

try:
    while True:
        currtime = datetime.now().strftime('%H:%M:%S')
        lux = light.light()

        leds.on()
        get_outside()
        get_temps()
        write_file()
        send_message()
        out.flush()
        leds.off()

        time.sleep(15)

except KeyboardInterrupt:
    leds.off()
    out.close()
