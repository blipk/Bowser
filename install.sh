sudo apt install python3 python3-tk
sudo yum install python3 python3-tkinter

mkdir ~/.config/bowser
cp bowser.py ~/.config/bowser/
chmod +777 ~/.config/bowser/bowser.py
sudo cp bowser.desktop /usr/share/applications
sudo chmod +777 /usr/share/applications/bowser.desktop
sudo cp bowser.svg /usr/share/icons/hicolor/scalable/apps
sudo cp bowser.png /usr/share/icons/hicolor/256x256/apps
python3 ~/.config/bowser/bowser.py
