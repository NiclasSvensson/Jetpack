# SonarSubmarine
A Jetpack Joyride like game developed in Python, using the Pygame library for GUI. Created as a hobby project to practice my signal processing ability. The Submarine is controlled by keeping a tone with a frequency. The thrust of the submarine is increased by increasing the frequency of the tone.

# Install
Developed on python 3.8.10. Create a python-venv, activate it and perform the following steps:

```
git clone git@github.com:NiclasSvensson/SonarSubmarine.git
cd SonarSubmarine
pip3 install -r requirements.txt
sudo apt-get install python3-tk
sudo apt-get install libportaudio2
```

# Run
```
cd src/
python3 main.py
```