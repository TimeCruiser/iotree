from flask import Flask
from flask_restful import Resource, Api
from flask import request
import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 32*5
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

app = Flask(__name__)
api = Api(app)

mode = 'off'

class LEDStrip(Resource):
    def get(self):
        return {'mode': mode}
    def put(self):
        global mode
        mode = request.data
        switcher = {
            'off': led_off,
            'rainbow_cycle': rainbow_cycle
        }
        func = switcher.get(mode, lambda pixels: 'invalid mode')
        result = func(pixels)
        return {'status': result, 'mode': mode}

api.add_resource(LEDStrip, '/led')

# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)

def rainbow_cycle(pixels, wait=0.01):
    j = 0
    while mode == "rainbow_cycle":
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
        # continuously cycle through all 256 colors in the wheel
        j = (j+1) % 256
    pixels.clear()
    pixels.show()
    return 'ok'

def led_off(pixels):
    pixels.clear()
    pixels.show()
    return 'ok'

if __name__ == '__main__':
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    # Start the web server
    app.run(debug=True, threaded=True, host='0.0.0.0')