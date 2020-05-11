# Dubois
Dubois is a DIY robot. It is designed to be fully customizable and modular, making it easy to upgrade (or downgrade) if you need to.
Dubois allows you to build a robot from scratch without having to follow strict guidelines or using specific parts. It grants the creator full control of the building process. These principles can be applied to tiny cheap affordable robots and bigger more sophisticated ones.

# Features
### Current
- Full motion control through the web client

### Future
- Speed control through PWM
- Headlight control
- Recording, taking snapshots and streaming video through Raspberry Pi camera
- Motion detection
- Obstacle detection
- Sensor support
- Measure battery life and notify user when battery levels drop.
- Add AI so it can be commanded through voice.

# Getting started
## Setup Wi-Fi and SSH.
- Download the [latest Raspbian image](https://www.raspberrypi.org/downloads/raspbian).
- Burn the image to a microSD card of your choice (at least 2GB in size).
- Mount the microSD card. Navigate to `/boot`.
- Create a file called "wpa_supplicant.conf" with the following details:
```
country=US
ctrl_interfac=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="MyWifiNetwork"
    psk="WifiPassword"
    key_mgmt=WPA-PSK
}
```
- Create a file called "ssh" in the same directory.

## Set up Pi camera.
- Open ***raspi-config***.
```sh
$ sudo raspi-config
```
- Select ***Interfacing Options > Pi Camera***
- Enable camera.

## Set up environment.
- SSH into the Pi. The default password is "raspberry".
```sh
$ ssh pi@raspberrypi.local
```
- Download and install dependencies.
```sh
$ sudo apt update
$ sudo apt install python3-pip
$ sudo apt install python3-picamera
$ sudo apt install rpi.gpio

# Python dependencies
$ sudo pip3 install flask
$ sudo pip3 install flask-socketio
```

## Finally, set up Dubois.
To set up, you must clone the repository, run `setup.sh` and reboot the Pi.
```sh
$ git clone https://www.github.com/obeezzy/dubois.git
$ cd dubois
$ sudo ./setup.sh
$ sudo reboot
```
Once booted, reconnect to Pi and retrieve hostname.
```sh
$ ssh pi@raspberrypi.local
$ hostname -I
```

If you complete these steps without error, then congratulations, you have successfully set up Dubois! To control Dubois, you need to:
- Connect your computer/phone to the same Wi-Fi used by Dubois.
- Connect to the web client by typing the following in the address bar of the browser of your choice on your computer/phone:
```sh
<pi-address>:5000
```
where **<pi-address>** should be replaced by the IP address of the Raspberry Pi.

# Software Architecture
Dubois is written mostly in **Python**. The **Flask** framework is used for the server. There is also a Web client written in HTML that is used as a convenient way to control Dubois without having to install the client on your phone.

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
