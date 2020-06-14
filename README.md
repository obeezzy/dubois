# Dubois
<div style='dislay: inline'>
<img alt='Raspberry Pi logo' src='https://github.com/obeezzy/dubois/blob/master/docs/images/pi-logo.svg' width='76' height='96'>
<img alt='Python logo' src='https://github.com/obeezzy/dubois/blob/master/docs/images/python-logo.svg' width='96' height='96'>
<img alt='HTML5 logo' src='https://github.com/obeezzy/dubois/blob/master/docs/images/html5-logo.svg' width='96' height='96'>
<img alt='CSS3 logo' src='https://github.com/obeezzy/dubois/blob/master/docs/images/css3-logo.svg' width='96' height='96'>
<img alt='JS logo' src='https://github.com/obeezzy/dubois/blob/master/docs/images/js-logo.svg' width='96' height='96'>
<img alt='Arrow sign' src='https://github.com/obeezzy/dubois/blob/master/docs/images/arrow-sign.svg' width='64' height='64'>
<img alt='Robot' src='https://github.com/obeezzy/dubois/blob/master/docs/images/robot.png' width='96' height='96'>
</div>
Dubois is a DIY robot. It is designed to be fully customizable and modular, making it easy to upgrade (or downgrade) if you need to.
Dubois allows you to build a robot from scratch without having to follow strict guidelines or using specific parts. It grants the creator full control of the building process. These principles can be applied to tiny cheap affordable robots and bigger more sophisticated ones.

# Features
### Current
- Full motion control through the web client
- Headlight control

### Future
- Speed control through PWM
- Recording, taking snapshots and streaming video through Raspberry Pi camera
- Motion detection
- Obstacle detection
- Sensor support
- Measure battery life and notify user when battery levels drop.
- Add AI so it can be commanded through voice.

# Getting started
## Setup Wi-Fi and SSH.
- Download the [latest Raspberry Pi OS Lite image](https://www.raspberrypi.org/downloads/raspberry-pi-os).
- Burn the image to a microSD card of your choice (at least 2GB in size).
- Mount the microSD card. Navigate to `/boot`.
- Configure the Wi-Fi settings on the Pi. Create a file called `wpa_supplicant.conf` with the following details:
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="MyWifiNetwork"
    psk="WifiPassword"
    key_mgmt=WPA-PSK
}
```
- Enable SSH. Create a file called `ssh` in the same directory.

## Set up environment.
- SSH into the Pi. The default password is `raspberry`.
```sh
$ ssh pi@raspberrypi.local
```
- Download and install dependencies.
```sh
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3-pip
$ sudo apt install python3-picamera
$ sudo apt install rpi.gpio
$ sudo apt install git

# Python dependencies
$ sudo pip3 install flask
$ sudo pip3 install websockets
```

## Set up Pi camera and SPI.
SPI is needed to receive input.
NOTE: The Pi camera feature is yet to be added.
- Open ***raspi-config***.
```sh
$ sudo raspi-config
```
- Select ***Interfacing Options > Pi Camera***
- Enable camera.
- Select ***Interfacing Options > SPI***.
- Enable SPI.

## Finally, set up Dubois.
First, retrieve your device's IP address. This is required to connect to the device through a browser later.
```sh
$ hostname -I
```
Now clone the repository, run `install_service.sh` and reboot the Pi.
```sh
$ git clone https://www.github.com/obeezzy/dubois.git
$ cd dubois
$ sudo ./install_service.sh
$ sudo reboot
```

If you complete these steps without error, then congratulations, you have successfully set up Dubois! To control Dubois, you need to:
- Connect your computer/phone to the same Wi-Fi used by Dubois.
- Connect to the web client by typing the following in the address bar of the browser of your choice on your computer/phone:
```sh
<pi-address>:4200
```
where **<pi-address>** should be replaced by the IP address of the Raspberry Pi.

## Set up Bluetooth (optional).
A Bluetooth speaker can be connect to Dubois as well. This later would be used for providing AI services.
- Install BlueAlsa.
```sh
$ sudo apt-get install bluealsa
```
- Start an instance of the BlueZ shell: `sudo bluetoothctl`.
- Turn off your Bluetooth speaker. This makes it easier to detect later on.
- While still in `bluetoothctl`, scan for devices: `scan on`.
- After about 3 seconds, turn on Bluetooth speaker. The speaker's device name should pop up within a few seconds.
- Pair with device using its MAC address: `pair XX:XX:XX:XX:XX:XX`, where `XX:XX:XX:XX:XX:XX` represents your Bluetooth speaker's MAC address.
- Trust the speaker (if you do): `trust XX:XX:XX:XX:XX:XX`.
- Connect to the speaker using `connect XX:XX:XX:XX:XX:XX`. If this attempt fails, run `sudo reboot` and try again.
- Copy `config/example_asoundrc` from the `dubois` folder to `~/.asoundrc`.
- Modify `~/.asoundrc` using your favorite editor. Replace all MAC address occurrences with your speaker's MAC address.
- Download a test `wav` file: `wget -O /tmp/test.wav https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav`
- Test Bluetooth speaker output: `aplay -D speaker /tmp/test.wav`.
- Test Bluetooth microphone input: `arecord -D mic -d 5 -f cd test.wav -c 1`.
- Test playback after recording: `aplay -D speaker test.wav`.


# Software Architecture
Dubois is written mostly in **Python**. The **Flask** framework is used for the server.
There is also a Web client written in HTML5, CSS3 and JavaScript (ES7) that is used as a convenient way to control Dubois without having to install the client on your phone.

### Flowchart
Coming soon.

# Hardware Architecture
### Circuit Diagram
![Circuit diagram](https://github.com/obeezzy/dubois/blob/master/docs/images/v0.1.0.png)

### Parts List
You will need the [Actobotics Peewee Runt Rover Kit](https://www.microcenter.com/product/449366/peewee-runt-rover-kit) or its equivalent. It's basically any kit that can stand on two wheels and has two motors. The components associated with diagram are listed below.
| Component | Value |
|-----------|-------|
| **R1-4** | 330R (x4) |
| **LED1-2** | Bright white LEDs (x2) |
| **LED3** | Tricolor LED (x1) |
| **B1** | Small cylindrical 5V power bank battery (x1) |
| **B2** | 6V AA battery pack (x1) |
| **CMR1** | Raspberry Pi Camera Module V2 (x1) |
| **IC1** | Raspberry Pi Zero W (x1) (All pin numbers shown are BCM) |
| **IC2** | L293D Quadruple Half H-Bridge Driver (x1) |
| **M1-2** | Rover motors (x2) |

# Todo
- Add documentation describing full workings of the system.
- Simplify setup process.

# License
MIT
