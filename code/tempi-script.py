import time
import math
import vcgencmd
import os
import json
import requests

from datetime import datetime
from envirophat import light, weather, leds

hook = os.environ["SLACK_WEBHOOK"]

out = open('enviro.log', 'w')
# out.write('Time\tTemp (Sensor)\tTemp (Calculated)\tTemp (Rounded)\tCPU Temp\tLight\n')
out.write('Time\tTemp (Sensor)\tTemp (Calibrated)\tCPU Temp\n')

factor = 0.882461847

try:
    while True:
        leds.on()
        currtime = datetime.now().strftime('%H:%M:%S')
        lux = light.light()
        cpu_temp = vcgencmd.measure_temp()
        temp = weather.temperature()
        temp_calibrated = temp - ((cpu_temp - temp)/factor)
        tempmed = '{:.1f}'.format(round(temp_calibrated, 2))
        # out.write('%s\t%f\t%f\t%s\t%f\t%s\n' % (currtime, temp, temp_calibrated, tempmed, cpu_temp, lux))
        # out.write('%s\t%f\t%f\n' % (currtime, temp, cpu_temp))
        out.write('%s\t%f\t%f\t%f\n' % (currtime, temp, temp_calibrated, cpu_temp))
        out.flush()
        message = "It is " + str(currtime) + "\nThe current temperature is " + str(tempmed) + " measuring " + str(lux) + " lux of light"
        payload = {'text':message}
        # r = requests.post(hook, json=payload)
        leds.off()
        time.sleep(60)

except KeyboardInterrupt:
    leds.off()
    out.close()
