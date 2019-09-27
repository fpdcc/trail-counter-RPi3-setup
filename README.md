R Pi 3 set up help for trail counter.

# Items needed for counter:
* Raspberry Pi (We've tested this on model 3 B)
* SD with Raspian Jesse installed
* PIR sensor
* Pi Camera
* Huawei E303 Cellualar USB dongle with Sim card (we got both from Hologram.io)
* External Battery (Currently we are using a 14000 mAh batery)

Other things to help development but may or may not be neccessary
* HDMI cable
* Adafruit T-cobbler w/ serial cable
* Bread board

# How to connect to Raspberry Pi
SSH

???


# Trail Counter
### Step 1
run `rasp_pi_installs.sh` to install all software

### Test installations
???

???

???

### Step 2
Connect external sensors/devices

???

### Step 3
Create systemd service to run on boot

```bash
sudo nano /lib/systemd/system/trail_counter.service
```
```
 [Unit]
 Description=Start trail counter service
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python /home/pi/Public/trail-counter-RPi3-setup/counter.py > /home/pi/Public/trail_counter.log 2>&1
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

also

```bash
sudo systemctl status trail_counter.service
sudo journalctl -f -u trail_counter.service
```
(ctrl+c to exit journalctl command)

### To switch raspberry pi to headless (non-GUI) mode use:
`sudo raspi-config`
> Boot options

> Desktop / CLI

Then choose an option depending on your preference.
