#!/bin/bash
# Build tensorflowlite 2.0 for R Pi 3
# for python 3

# Taken from https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

DATA_DIR="/home/pi/Public/trail-counter-RPi3-setup"

# Get requirements file
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
