# LED Python Service

Python Flask web service providing control of the LED strip. To be deployed on the Raspberry Pi that's connected to the LED strip.

Basically a flask wrapper around [this tutorial to control a WS2801 LED strip](https://tutorials-raspberrypi.de/raspberry-pi-ws2801-rgb-led-streifen-anschliessen-steuern/).

## Prerequisites

* Python 2.7
* Flask-RESTful (`sudo pip install flask-restful`)
* AdaFruit WS2801 Library (`sudo pip install adafruit-ws2801`)
* Optional: Install the `iotree-led.service` file as described in its comments

The service must be run as root to be able to access the GPIO pins

## API

**Change operating mode**

`curl -X PUT -H "Content-Type: application/json" http://localhost:5000/led -d "<mode>"`

Valid values for `<mode>` are: `rainbow_cycle`, `flash_colors`, `off`

**Get current operating mode**

`curl -X GET http://localhost:5000/led`