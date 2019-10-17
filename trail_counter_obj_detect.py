#!/usr/bin/python

import numpy as np
import os
import sys
import requests
import datetime
import yaml
from PIL import Image
from tensorflow.lite.python.interpreter import Interpreter

# Env setup
config = yaml.safe_load(open("/home/pi/Public/config.yaml"))
CHANNELID = config['thingspeak']['CHANNELID']
KEY = config['thingspeak']['KEY']

# Arguments
MODEL_NAME = "/home/pi/Public/"
GRAPH_NAME = "/home/pi/Public/"
LABELMAP_NAME = "/home/pi/Public/"
min_conf_threshold = 0.5
IM_NAME = "counter_image.jpg"

CWD_PATH = os.getcwd()
print(CWD_PATH)

PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_NAME)
images = glob.glob(PATH_TO_IMAGES)
print(PATH_TO_IMAGES)
print(images)

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# If first label is '???', remove.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model and get details
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Load image and resize to expected shape [1xHxWx3]
image = Image.open(image_path)
imW, imH, _ = image.size
input_data = np.expand_dims(image, axis=0)

# Normalize pixel values if using a floating model (i.e. if model is non-quantized)
if floating_model:
    input_data = (np.float32(input_data) - input_mean) / input_std

# Perform the actual detection by running the model with the image as input
interpreter.set_tensor(input_details[0]['index'],input_data)
interpreter.invoke()

# Retrieve detection results
boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects	

# Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

    # All the results have been drawn on the image, now display the image
    cv2.imshow('Object detector', image)

# bicycle = 0
# person = 0
# horse = 0

# for d in detec:
    # if d['name'] == 'bicycle':
        # bicycle += 1
    # if d['name'] == 'person':
        # person += 1
    # if d['name'] == 'horse':
        # horse += 1


# main_url = 'https://api.thingspeak.com/update?api_key=' + KEY
# channel_id = CHANNELID
# date = str(datetime.datetime.now())
# payload = dict(field1=date, field3=bicycle, field4=person, field5=horse)

# for attempt in range (10):
    # try:
        # r = requests.post(main_url, params=payload)
        # print r.url
        # print 'payload sent'
    # except requests.exceptions.ConnectionError:
        # print 'Connection Error'
        # pass
    # else:
        # break

# print 'bicycle =', (bicycle)
# print 'person =', (person)
# print 'horse =', (horse)
