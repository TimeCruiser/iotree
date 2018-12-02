from flask import Flask
from flask_restful import Resource, Api
from flask import request

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
            'off': led_off
        }
        func = switcher.get(mode, lambda: 'invalid mode')
        result = func()
        return {'status': result, 'mode': mode}

api.add_resource(LEDStrip, '/led')

def led_off():
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')