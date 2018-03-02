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
    filename = datetime.strftime(datetime.now(),'%Y-%m-%d-%H-%M-%S')
    piclocation = '/home/pi/Pictures/'+ filename + '.jpg'
    time.sleep(1)
    camera.capture(piclocation)
    camera.close()
        

print("PIR Module test")
time.sleep(2)
print("Ready")

#    while True:
#        if io.input(pir_pin):
#            print("Motion Detected")
#        time.sleep(1)

#io.remove_event_detect(pir_pin)
#time.sleep(2)

#try:
#    io.add_event_detect(pir_pin, io.RISING, callback=motion)
#    while 1:
#            time.sleep(1)
#except KeyboardInterrupt:
#        print "Quit"
#        io.cleanup()
#

while True:
    try:
        print "rpi-ms-camera: Waiting for motion."
        io.wait_for_edge(pir_pin, io.RISING)
        motion(pir_pin)
        print "rpi-ms-camera: Sleeping "
        time.sleep(1)
    except KeyboardInterrupt:
        print "rpi-ms-camera: Stopping due to keyboard interrupt."
        camera.close()
        io.cleanup()
        break

