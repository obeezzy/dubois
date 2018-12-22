# Dubois
Dubois is a DIY robot. It is designed to be fully customizable and modular, making it easy to upgrade (or downgrade) if you need to.
Dubois allows you to build a robot from scratch without having to follow strict guidelines or using specific parts. It grants the creator full control of the building process. These principles can be applied to tiny cheap affordable robots and bigger more sophisticated ones.

# Features
### Current
- Full motion control through the Dubois Web client

### Future
- Speed control through PWM
- Headlight control
- Recording, taking snapshots and streaming video through Raspberry Pi camera
- Motion detection
- Create Dubois Flutter client
- "Follow me" feature
- Temperature sensing
- Obstacle detection
- Distance measuring
- Speed measuring
- Measure battery life and notify user when battery levels drop.
- Add AI so it can be commanded through voice.

# Prerequisites
- The Raspberry Pi used must have the Raspbian OS installed on it.
- You must enable SSH and the camera module using ***raspi-config***.
- The Raspberry Pi must be connected to your local (preferably home) Wi-Fi.

# Getting started
To set up, you must clone the repository, create a virtual environment and then install all dependencies listed in the **requirements.txt** file.
```sh
$ git clone https://www.github.com/obeezzy/dubois.git
$ cd dubois
$ python3 -m pip install --user virtualenv
$ python3 -m virtualenv env
$ pip install -r requirements.txt
```
Next, if your Raspberry Pi is connected to your local Wi-Fi, you need to get its IP address using the following comand:
```sh
$ hostname -I
```
To start the application, execute the following:
```sh
$ python3 main.py
```
If you complete these steps without error, then congratulations, you have successfully set up Dubois! To control Dubois, you need to:
- Connect your phone to the same Wi-Fi used by Dubois.
- Connect to Dubois' Web client by typing the following in the browser of your choice on your phone:
```sh
<ip-address>:5000
```
where **<ip-address>** should be replaced by the IP address of the Raspberry Pi.

# Software Architecture
Dubois is written mostly in **Python**. The **Flask** framework is used for the server. There is also a Web client written in HTML that is used as a convenient way to control Dubois without having to install the client on your phone.

### Flowchart
Coming soon.

# Hardware Architecture
### Circuit Diagram
![Circuit diagram](https://www.github.com/obeezzy/dubois/docs/images/v0.1.0.png)

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


