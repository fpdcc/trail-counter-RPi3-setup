import RPi.GPIO as io
import time
from picamera import PiCamera
from datetime import datetime

#PIR setup
pir_pin = 17
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
    filename = datetime.strftime(datetime.now(),'%Y-%m-%d-%H-%M-%S')
    piclocation = '/home/pi/Pictures/'+ filename + '.jpg'
    time.sleep(1)
    camera.capture(piclocation)
        

print("PIR Module test")
time.sleep(2)
print("Ready")

while True:
    try:
        print ("rpi-ms-camera: Waiting for motion.")
        io.wait_for_edge(pir_pin, io.RISING)
        motion(pir_pin)
        print ("rpi-ms-camera: Sleeping")
        time.sleep(1)
    except KeyboardInterrupt:
        print ("rpi-ms-camera: Stopping due to keyboard interrupt.")
        camera.close()
        io.cleanup()
        break
