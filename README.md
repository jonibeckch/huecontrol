# simplehue
A simple Project to control your hue lights with a raspberrypi, by opening pages on your local network

# Current Status
## A bit slow
Access through SSH is super slow at the moment. Could be either a network issue or related to the local.rc. To be checked...

# Troubleshooting

## Deploy Flask to WSGI Server for reliable use
Flask is not designed to be run as a productive system. It should be deployed to as WSGI Server. Nevertheless due to minimize the effort it is currently used like this. For further Info see:
https://flask.palletsprojects.com/en/stable/deploying/

## Run on startup with local.rc

There is a way to use local.rc to run the python on startup. It is usually not recommended but worked so far. The local.rc will be run as an admin. So it makes sense to run the command which is put into the local.rc beforehand with a "sudo" added before, to see if the python libraries are installed and working also for the admin user!
```sudo python3 /home/pi/huecontrol/home.py``` 

Use Nano the edit the local.rc file
```sudo nano /etc/rc.local```
1. Outcomment the "exit 0" in the end, otherwise the program will stop again.
2. add the command to run the python file "python3 /home/pi/huecontrol/home.py" via nano

In this case "python3" has been used as "python" is not working if run as python in rc.local.




# Running on Raspian Version 12
```
cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
```

Step 1:
pip install flask phue



