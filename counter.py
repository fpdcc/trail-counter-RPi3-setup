import RPi.GPIO as io
import time
from picamera import PiCamera
from datetime import datetime

#PIR setup
pir_pin = 4
io.setmode(io.BCM)
io.setup(pir_pin, io.IN)

#camera settings
camera = PiCamera()
camera.exposure_mode = 'auto'
camera.image_effect='blur'
camera.resolution = (400, 300)
camera.awb_mode = 'auto'

def motion(pir_pin):
        print("Motion!")
        filename = datetime.strftime(datetime.now(),'%Y-%m-%d-%H-%M')
        piclocation = '/home/pi/Pictures/'+ filename + '.jpg'
        time.sleep(1)
        camera.capture(piclocation)
        camera.close()
        file.close()
        time.sleep(1)
        return send_file(piclocation)
        

print("PIR Module test")
time.sleep(2)
print("Ready")

#    while True:
#        if io.input(pir_pin):
#            print("Motion Detected")
#        time.sleep(1)

io.remove_event_detect(pir_pin)
sleep(2)
io.add_event_detect(pir_pin, io.RISING, callback=motion)

