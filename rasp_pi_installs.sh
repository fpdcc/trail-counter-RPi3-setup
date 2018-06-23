# Build tensorflow for R Pi 3
# for python 3

mkdir tensorflow_obj_det
cd tensorflow_obj_det

sudo apt-get update
sudo apt-get install -y wget git unzip build-essential python3-pip python3-dev libblas-dev liblapack-dev libatlas-base-dev gfortran

pip3 install lxml numpy pandas requests urllib3 protobuf==3.0.0 pyyaml
pip3 install --user http://ci.tensorflow.org/view/Nightly/job/nightly-pi-python3/lastStableBuild/artifact/output-artifacts/tensorflow-1.8.0-cp34-none-linux_armv7l.whl
pip3 uninstall mock
pip3 install --user mock
rm tensorflow-1.8.0-cp34-none-linux_armv7l.whl

# Clone tensorflow models
git clone https://github.com/tensorflow/models.git

# Clone our trained models
git clone https://github.com/glw/tensorflow_trained_models.git

# Install protoc3
wget https://github.com/google/protobuf/releases/download/v3.0.0/protobuf-cpp-3.0.0.zip
unzip protobuf-cpp-3.0.0.zip -d protoc3
cd  protoc3/protobuf-3.0.0
# ./autogen.sh
./configure --prefix=/usr
sudo make
sudo make check
sudo make install
sudo ldconfig
cd ../
rm protoc-3.0.0-linux-x86_64.zip

# check version
echo 'checking protoc version'
echo protoc --version

# move into tensorflow models repo
cd models/research

# run requirement for tensorflow
protoc object_detection/protos/*.proto --python_out=.

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

cd object_detection/
python3 setup.py build && \
python3 setup.py install

cd ../
cd slim/
python3 setup.py build && \
python3 setup.py install
