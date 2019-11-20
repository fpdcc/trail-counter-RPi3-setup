# R Pi 3 set up help for trail counter.

![Raspberry Pi trail counter](https://raw.githubusercontent.com/fpdcc/trail-counter-RPi3-setup/master/img/trail_counter55.jpg)


# Items needed for counter:
* Raspberry Pi (We've tested this on model 3B+ - with headers)
* SD with Raspian Buster installed
* PIR sensor
* Pi Camera
* Huawei E303 Cellualar USB dongle with Sim card (we got both from Hologram.io)
* External Battery (Currently we are using a Ravpower 26800 mAh battery)
* [ThingSpeak](thingspeak.com) account and API key

Other things to help development or in constructing the sensor - these are not neccessary
* HDMI cable
* Adafruit T-cobbler w/ serial cable
* Bread board
* 12in camera cable
* female to female wires

#### ThingSpeak Account

Once you sign upfor an account, create a channel. Select your channel and add field names according to those found in the detect.py file.

- Field 1 = current_date
- Field 2 = last_date
- Field 3 = bicycle
- Field 4 = person
- Field 5 = horse
- Field 6 = car

Then Click on API Keys and Generate New Write API Key, copy key and save for step 3.

# Trail Counter

### Step 1

```cd /home/pi/Public/```

Then

```
git clone https://github.com/fpdcc/trail-counter-RPi3-setup.git
cd trail-counter-RPi3-setup
./rasp_pi_installs.sh
```

### Step 2

Connect external sensors/devices

Connect PIR sensor
 1. GND on sensor to a ground pinon the pi.
 2. 5v pin to 5v pin on pi.
 3. out pin to xxx pin on pi.

Allow camera
```sudo raspi-config```

select
 > Interface options
   > Camera
     > YES

Connect Raspberry Pi Camera Rev 1.3
 1.Ribbon cable from camera goes into slot labeled camera on pi.

Plug in Huawei E303 3G Wireless into USB port

### Step 3

Update sample_config.py, rename to config.py and put in your own ThingSpeak API KEY and CHANNELID.

### Step 4

Create systemd service to run on boot

```bash
sudo nano /lib/systemd/system/trail_counter.service
```
Copy and paste into file


```
 [Unit]
 Description=Start trail counter service
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python /home/pi/Public/trail-counter-RPi3-setup/counter.py
 Restart=always

 [Install]
 WantedBy=multi-user.target

```

Exit nano

`ctrl+X` and `y` to save


```
sudo chmod 644 /lib/systemd/system/trail_counter.service
sudo systemctl daemon-reload
sudo systemctl enable trail_counter.service
```

Reboot to start service

To check status of service use these tools
`top` or `htop`

Look for something called trailcounter.service

also systemctl and journalctl help to view logs of the service and troubleshoot issues.

```bash
sudo systemctl status trail_counter.service
sudo journalctl -f -u trail_counter.service
```

(ctrl+c to exit journalctl command)

To check log files after use in the field go to

```/var/log/syslog```

Each time the counter detect an object it printed the URL to the log file. This can be checked against what you are recieving in ThingSpeak.


### To switch raspberry pi to headless (non-GUI) mode use:


`sudo raspi-config`
> Boot options
  > Desktop / CLI

Then choose an option depending on your preference.

### To turn off bluetooth and wifi

`nano /boot/config.txt`

add lines

```
dtoverlay=pi3-disable-bt
dtoverlay=pi3-disable-wifi
```

---

# This section is not part of the set up for the Raspberry Pi

## To run object detection with Tensorflow Lite on an image.

* [detect.py was adapted from the original TensorFlow git repository](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)

```
python3 detect.py \
--model detect.tflite \
--labels coco_labels.txt \
--threshold 0.55 \
--image /home/pi/Public/images/counter_image.jpg
```

Currently detect.py has default values set so you dont have to include any flags when running it as specified above.
