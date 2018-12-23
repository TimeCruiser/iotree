from flask import Flask
from flask_restful import Resource, Api
from flask import request
import time
import RPi.GPIO as GPIO
import random
 
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
        mode = request.json['mode']
        params = request.json['params']
        switcher = {
            'off': led_off,
            'rainbow_cycle': rainbow_cycle,
            'flash_colors': flash_colors,
            'eiffel_tower': eiffel_tower,
            'flame': flame,
            'solid_color': solid_color
        }
        func = switcher.get(mode, lambda pixels: 'invalid mode')
        result = func(pixels, params)
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

def rainbow_cycle(pixels, params, wait=0.01):
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

def flame(pixels, params, wait=0.1):
    j = 0
    while mode == "flame":
        for j in range(20,60):
            for i in range(pixels.count()):
                color = Adafruit_WS2801.RGB_to_color(255,j,0)
                pixels.set_pixel(i, color)
            pixels.show()
            if wait > 0:
                time.sleep(wait)
        for j in range(60,20,-1):
            for i in range(pixels.count()):
                color = Adafruit_WS2801.RGB_to_color(255,j,0)
                pixels.set_pixel(i, color)
            pixels.show()
            if wait > 0:
                time.sleep(wait)
    pixels.clear()
    pixels.show()
    return 'ok'

def flash_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        if mode != "flash_colors":
            break
        # blink two times, then wait
        pixels.clear()
        for j in range(3):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)

def flash_colors(pixels, params):
    while mode == "flash_colors":
        for i in range(3):
            flash_color(pixels, blink_times = 1, color=(255, 0, 0))
            flash_color(pixels, blink_times = 1, color=(0, 255, 0))
            flash_color(pixels, blink_times = 1, color=(0, 0, 255))
    pixels.clear()
    pixels.show()
    return 'ok'

def eiffel_tower(pixels, params):
    white = Adafruit_WS2801.RGB_to_color(255, 255, 255)
    while mode == "eiffel_tower":
        for i in range(20):
            j = random.randint(0, pixels.count()-1)
            pixels.set_pixel(j, white)
        pixels.show()
        time.sleep(0.02)
        pixels.clear()
        pixels.show()
        time.sleep(0.02)
    return 'ok'

def solid_color(pixels, params):
    color = Adafruit_WS2801.RGB_to_color(params['r'], params['g'], params['b'])
    for i in range(pixels.count()):
        pixels.set_pixel(i, color)
    pixels.show()
    return 'ok'

def led_off(pixels, params):
    mode = 'off'
    pixels.clear()
    pixels.show()
    return 'ok'

if __name__ == '__main__':
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    # Start the web server
    app.run(debug=True, threaded=True, host='0.0.0.0')