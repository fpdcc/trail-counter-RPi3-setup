#!/bin/bash
# Build tensorflowlite 2.0 for R Pi 3
# for python 3

# Taken from https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

DATA_DIR="/home/pi/Public/trail-counter-RPi3-setup"

# Install Tensorflow Lite
python3 -m pip install tflite_runtime-1.14.0-cp37-cp37m-linux_armv7l.whl

# Get requirements for object detection with PiCamera
curl -O https://raw.githubusercontent.com/tensorflow/examples/master/lite/examples/object_detection/raspberry_pi/requirements.txt

# Install required packages
python3 -m pip install -r requirements.txt
python3 -m pip install pyaml

# Get TF Lite model and labels
curl -O http://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
unzip coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip -d ${DATA_DIR}
rm coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip

# Get a labels file with corrected indices, delete the other one
(cd ${DATA_DIR} && curl -O  https://dl.google.com/coral/canned_models/coco_labels.txt)
rm ${DATA_DIR}/labelmap.txt
