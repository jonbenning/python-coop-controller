import argparse
import board
import datetime
import sys
import yaml
from suntime import Sun, SunTimeException
from gpiozero import Button, LED
from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import config_schema

app = Flask(__name__)

api = Api(app)

class ChickenPi():
    '''
    This class implements the physical hardware needed for
    the automated chicken door. including anything relating to
    raspi gpio, the movement of motors, and limit switches.
    '''
    def __init__(self,open_limit,close_limit, obs_limit):
        #kit = MotorKit(i2c=board.I2C())
        self.open_limit_switch = Button(open_limit,bounce_time=0.2)
        self.close_limit_switch = Button(close_limit,bounce_time=0.2)
        self.obs_limit_switch = Button(obs_limit,bounce_time=0.2)
        self.door_travel_steps = self.find_limits()

    def find_limits(self):
        '''This function will open, close, and open the door to find its limits'''
        # check the current states of the limits
        # open the door if not open.
        # close the door, record the step count
        # open the door, record the step count
        # check if the step counts match. do something if they don't?
        # return the step count
        step_count = 100
        return step_count

    def close(self):
        pass

    def open(self):
        pass

    def monitor(self):
        self.open_limit_switch.when_pressed = self.button_pressed
        self.open_limit_switch.when_released = self.button_released
        self.close_limit_switch.when_pressed = self.button_pressed
        self.close_limit_switch.when_released = self.button_released
        self.obs_limit_switch.when_pressed = self.button_pressed
        self.obs_limit_switch.when_released = self.button_released

    def button_pressed(self):
        print("button was pressed")
    
    def button_released(self):
        print("button was released")

class Scheduler():
    '''
    This class deals with time, sunrise, sunset, and trigger events
    against the hardware to enable things like automated open/close
    at sunrise or sunset. If scheduler is disabled open and close
    events are only triggered via api/webpage requests.
    '''
    def __init__(self,latitude, longitude, sunrise_offset, sunset_offset):
        self.latitude = latitude
        self.longitude = longitude
        self.sun = Sun(self.latitude,self.longitude)
        self.today_sr = self.sun.get_sunrise_time().timestamp()
        self.today_ss = self.sun.get_sunset_time().timestamp()


class DoorStatus(Resource):
    def __init__(self, **kwargs):
        self.schedule = kwargs['schedule']
        self.door = kwargs['door']

    def get(self):
        open_limit_status = self.door.open_limit_switch.value
        close_limit_status = self.door.close_limit_switch.value
        obs_limit_status = self.door.obs_limit_switch.value
        return jsonify({"open_limit": open_limit_status,"close_limit": close_limit_status, "obstruction_limit": obs_limit_status})
        #return jsonify({"sunrise": f"{self.schedule.today_sr}","sunset": f"{self.schedule.today_ss}"})

def load_config(filename):
    with open(filename, 'r') as file:
        yaml_config = yaml.safe_load(file)
        if config_schema.check(yaml_config):
            return yaml_config
        else:
            print("invalid yaml configuration")
            sys.exit(1)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    config = load_config(args.filename)
    pins = config['pins']
    location = config['location']
    schedule = config['schedule']

    door = ChickenPi(**pins)
    sched = Scheduler(**location,**schedule)

    api.add_resource(DoorStatus, '/api/door', resource_class_kwargs={"schedule": sched,"door": door})
    #api.add_resource(SchedStatus, '/api/status/sched', resource_class_kwargs={"schedule": sched,"door": door})
    door.monitor()
    app.run(host='0.0.0.0', debug = True)
