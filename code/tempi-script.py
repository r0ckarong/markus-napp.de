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
#out.write('time\tlight\trgb\tmotion\theading\ttemp\tpress\n')
out.write('Time\tTemp (Sensor)\tTemp (Calculated)\tTemp (Rounded)\tCPU Temp\tLight\n')

factor = 0.819602564265192

try:
    while True:
        leds.on()
        currtime = datetime.now().strftime('%H:%M:%S')
        lux = light.light()
        cpu_temp = vcgencmd.measure_temp()
        temp = weather.temperature()
        temp_calibrated = temp - ((cpu_temp - temp)/factor)
        tempmed = round(temp_calibrated, 0)
        #tempmed = 0.5 * math.ceil(2.0 * weather.temperature())
        press = weather.pressure()
        #out.write('%s\t%f\t%s\t%s\t%f\t%f\t%f\n' % (currtime, lux, rgb, acc, heading, temp, press))
        out.write('%s\t%f\t%f\t%i\t%f\t%s\n' % (currtime, temp, temp_calibrated, tempmed, cpu_temp, lux))
        out.flush()
        message = "It is " + str(currtime) + "\nThe current temperature is " + str(tempmed) + " measuring " + str(lux) + " lux of light"
        payload = {'text':message}
        #r = requests.post(hook, json=payload)
        leds.off()
        time.sleep(60)

except KeyboardInterrupt:
    leds.off()
    out.close()
