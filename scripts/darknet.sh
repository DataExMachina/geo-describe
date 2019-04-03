echo "Download darknet"
wget https://github.com/pjreddie/darknet/archive/master.zip
unzip master.zip
rm master.zip

echo "Download weights"
cd darknet-master/
sudo wget https://pjreddie.com/media/files/yolov3-tiny.weights

echo "Compile darknet"
make
