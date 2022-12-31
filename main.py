#!/usr/bin/python3

import argparse
import board
import datetime
from datetime import datetime 
import sys
import yaml
from suntime import Sun, SunTimeException
from gpiozero import Button, LED
import RPi.GPIO as GPIO
from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from gpiozero.pins.native import NativeFactory
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
        self.open_limit_switch = Button(open_limit,pull_up=False)
        self.close_limit_switch = Button(close_limit,pull_up=False)
        self.obs_limit_switch = Button(obs_limit,pull_up=False)


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
        self.open_limit_switch.when_released = self.nc_limit_opened
        self.close_limit_switch.when_released = self.nc_limit_opened
        self.obs_limit_switch.when_released = self.nc_limit_opened


    def nc_limit_opened(self,switch):
        '''
        Limit switches are Normally Closed (NC). This function triggers when 
        those switches are opened - i.e. when a limit is hit.
        '''
        print(f"limit on pin {switch.pin.number} was opened at {datetime.timestamp(datetime.now())}")


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

    #def put(self,

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
    app.run(host='0.0.0.0', debug = True, use_reloader=False)
