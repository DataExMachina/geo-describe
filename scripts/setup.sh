echo "Create virtual Python env."
virtualenv -p python3 .venv

echo "Install Python packages"
source .venv/bin/activate
pip3 install -r requirements.txt
deactivate
