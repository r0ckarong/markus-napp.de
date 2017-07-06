import time
import math
import vcgencmd
import os
import json
import requests
import schedule

from datetime import datetime
from envirophat import light, weather, leds

# raspi = :raspberry_pi:

# Declaring global variables
temp = 0
tempmed = 0
temp_calibrated = 0
cpu_temp = 0
outside_temp = 0
outside_location = ""
outside_condition = ""
currtime = datetime.now().strftime('%H:%M:%S')

# Slack Webhook stored in filesystem
slack_webhook = os.environ["SLACK_WEBHOOK"]

# Data for Openweathermap Query
owm_key = os.environ["OWM_KEY"]
zip_code = "60433"
country_code = "de"
unit = "metric"

# Sensor offset factor
factor = 0.868218182

# Open log file for temp data
out = open('enviro.log', 'w')
out.write('Time\tTemp (Sensor)\tTemp (Calibrated)\tTemp (Rounded)\tCPU Temp\n')

def get_condition():
    """
    TODO

    Reads current condition and maps emoji and icons to the message which is to be sent to Slack.
    """

def get_outside():
    """
    Polls the weather data from openweathermap API and returns values for global usage.

    Will be refactored to use pyowm instead of requests.
    """
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

    post = """It is currently %s in %s, %s\nOutside there is "%s" at %s C\nInside the office we have a temperature of %s C
    """

    message = post % (mytime, zip_code, outside_location, outside_condition, out_temp, med)

    # print message

    payload = {'text':message}
    requests.post(slack_webhook, json=payload)

def write_file():
    out.write('%s\t%f\t%f\t%s\t%f\n' % (currtime, temp, temp_calibrated, tempmed, cpu_temp))

def write_json():
    date = datetime.now().strftime('%d-%m-%Y')

    json_file = open('weather.json', 'w')
    weather = [json_file]
    data = {
    'temperature':tempmed,
    'outside_temp':outside_temp,
    'outside_condition':outside_condition,
    'outside_location':outside_location,
    'time':currtime,
    'date':date
    }
    json_file.append(data)
    #json.dump(data, json_file, indent=4)
    json_file.flush()

def perform_update():
    global currtime
    currtime = datetime.now().strftime('%H:%M:%S')
    lux = light.light()
    leds.on()
    get_outside()
    get_temps()
    write_file()
    # write_json()
    # send_message()
    out.flush()
    leds.off()

# Schedule messages
schedule.every().day.at("08:00").do(send_message)
schedule.every().day.at("12:00").do(send_message)

try:
    while True:
        perform_update()

        schedule.run_pending()

        time.sleep(30)

except KeyboardInterrupt:
    leds.off()
    out.close()
    # json_file.close()
