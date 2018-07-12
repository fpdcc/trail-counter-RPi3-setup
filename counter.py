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
camera.resolution = (680, 480)
camera.awb_mode = 'auto'

def motion(pir_pin):
    # print("Motion!")
    filename = 'counter_image.jpg'
    piclocation = '/home/pi/Public/'+ filename
    time.sleep(1)
    # camera.start_preview()
    # time.sleep(2)
    camera.capture(piclocation)
    time.sleep(1)
    # camera.stop_preview()


# print("PIR Module test")
time.sleep(2)
# print("Ready")

while True:
    try:
        # print ("rpi-ms-camera: Waiting for motion.")
        io.wait_for_edge(pir_pin, io.RISING)
        motion(pir_pin)
        time.sleep(2)
	# print("executing object detection")
	execfile("/home/pi/Public/tensorflow_trained_models/trail_counter_obj_detect.py")
        # print ("rpi-ms-camera: Sleeping")
        # time.sleep(1)
    except KeyboardInterrupt:
        # print ("rpi-ms-camera: Stopping due to keyboard interrupt.")
        camera.close()
        io.cleanup()
        break
