from unicodedata import name
import RPi.GPIO as GPIO
from app_package import db, app
from app_package.models import Reading, Settings, Config
from time import sleep
from datetime import datetime, timedelta
from signal import signal, SIGINT
from sys import exit

def handler(signal_received, frame):
    # Handle any cleanup here
    print('\nSIGINT or CTRL-C detected. Cleaning up and exiting gracefully.')
    GPIO.cleanup()
    exit(0)
    
signal(SIGINT, handler)

# TODO: 
#   wire button in for manual pump override

PUMP_LIGHT_PIN = 26
PUMP_PIN = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PUMP_LIGHT_PIN, GPIO.OUT)
GPIO.setup(PUMP_PIN, GPIO.OUT)

with app.app_context():
    while True:
        config = Config.query.filter_by(id = 1).first()
        active_profile_settings = config.active_profile.settings
        
        pump_duration_seconds = active_profile_settings.pumpCycleLength * 60
        pump_duration_seconds = 5

        print("On")
        GPIO.output(PUMP_LIGHT_PIN, GPIO.HIGH)
        GPIO.output(PUMP_PIN, GPIO.HIGH)
        sleep(pump_duration_seconds)
        
        print("off")
        GPIO.output(PUMP_LIGHT_PIN, GPIO.LOW)
        GPIO.output(PUMP_PIN, GPIO.LOW)
        sleep(pump_duration_seconds)
        





