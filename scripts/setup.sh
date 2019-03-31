# echo "Create virtual Python env."
# virtualenv .venv
#
# echo "Install Python packages"
# source .venv/bin/activate
# pip3 install -r requirements.txt
# deactivate

echo "Build darknet / yolov3"
git clone ssh://git@github.com/pjreddie/darknet
cd darknet
make
sudo wget https://pjreddie.com/media/files/yolov3.weights
