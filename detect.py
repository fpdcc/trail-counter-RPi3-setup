# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TF Lite to detect objects with the Raspberry Pi camera."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import datetime
import yaml
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

config = yaml.safe_load(open("/home/pi/Public/trail-counter-RPi3-setup/config.yaml"))
#CHANNELID = config['thingspeak']['CHANNELID']
KEY = config['thingspeak']['KEY']


def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels


def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results


lbl = []
def annotate_objects(results, labels):
  """Returns labels and scores for an inference"""
  for obj in results:
    lbl.append([labels[obj['class_id']], obj['score']])
  return lbl

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=True)
  parser.add_argument(
      '--labels', help='File path of labels file.', required=True)
  parser.add_argument(
      '--threshold',
      help='Score threshold for detected objects.',
      required=False,
      type=float,
      default=0.4)
  parser.add_argument(
      '--image',
      help='Path to image. Eg. /path/to/image/imageName.jpg',
      required=True)
  args = parser.parse_args()

  labels = load_labels(args.labels)
  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  with Image.open(args.image).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS) as f:
      results = detect_objects(interpreter, f, args.threshold)
      detect = annotate_objects(results, labels)
      print(type(detect))
      print(detect)

      bicycle = 0
      person = 0
      horse = 0
      car = 0

      for d in detect:
          if d[0] == 'bicycle':
              bicycle += 1
          if d[0] == 'person':
              person += 1
          if d[0] == 'horse':
              horse += 1
          if d[0] == 'car':
              car += 1


      main_url = 'https://api.thingspeak.com/update?api_key=' + KEY
      date = str(datetime.datetime.now())
      payload = dict(field1=date, field3=bicycle, field4=person, field5=horse, field6=car)

      for attempt in range (10):
          try:
              r = requests.post(main_url, params=payload)
              print(r)
              print(r.url)
              # print 'payload sent'
          except requests.exceptions.ConnectionError:
              # print 'Connection Error'
              pass
          else:
              break

      print('bicycle ={}'.format(bicycle))
      print('person ={}'.format(person))
      print('horse ={}'.format(horse))
      print('car ={}'.format(car))

if __name__ == '__main__':
  main()
