
import datetime
import board
from suntime import Sun, SunTimeException
from gpiozero import Button, LED
from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

app = Flask(__name__)

api = Api(app)

#def setup_motor():
#    kit = MotorKit(i2c=board.I2C())

class Hello(Resource):
    def get(self):
        latitude = 45.3256
        longitude = 93.9395
        sun = Sun(latitude,longitude)
        today_sr = sun.get_sunrise_time()
        today_ss = sun.get_sunset_time()
        #return jsonify({'message': 'hello world'})
        return jsonify({"sunrise": f"{sun.get_sunrise_time()}","sunset": f"{sun.get_sunset_time()}"})

api.add_resource(Hello, '/')

if __name__=="__main__":
    app.run(host='0.0.0.0', debug = True)
