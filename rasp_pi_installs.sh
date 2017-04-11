#build tensorflow for R Pi 3 from
#https://github.com/samjabrahams/tensorflow-on-raspberry-pi

#for python 3
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.0.1/tensorflow-1.0.1-cp34-cp34m-linux_armv7l.whl
pip3 install --user tensorflow-1.0.1-cp34-cp34m-linux_armv7l.whl
pip3 uninstall mock
pip3 install --user mock
