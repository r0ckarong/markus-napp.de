import time
import math
from datetime import datetime
from envirophat import light, motion, weather, leds


out = open('enviro.log', 'w')
#out.write('time\tlight\trgb\tmotion\theading\ttemp\tpress\n')
out.write('Time\tTemperature\tTemp (Rounded)\tLight\tPressure\n')

try:
    while True:
        currtime = datetime.now().strftime('%H:%M:%S')
        lux = light.light()
        leds.on()
        rgb = str(light.rgb())[1:-1].replace(' ', '')
        leds.off()
        acc = str(motion.accelerometer())[1:-1].replace(' ', '')
        heading = motion.heading()
        temp = weather.temperature() - 6.1
        tempmed = round(temp, 0)
        #tempmed = 0.5 * math.ceil(2.0 * weather.temperature())
        press = weather.pressure()
        #out.write('%s\t%f\t%s\t%s\t%f\t%f\t%f\n' % (currtime, lux, rgb, acc, heading, temp, press))
        out.write('%s\t%f\t%i\t%s\t%f\n' % (currtime, temp, tempmed, lux, press))
        out.flush()
        time.sleep(20)

except KeyboardInterrupt:
    leds.off()
    out.close()
