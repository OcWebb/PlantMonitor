import RPi.GPIO as GPIO
from app_package import db
from app_package.models import Reading, Settings

from time import sleep

delay = 1
samples = 15


while True:
    
    settings = Settings.query.order_by(db.desc(Settings.timestamp)).all()

    print(len(settings))
    print(settings[0].serialize())

    sleep(delay)




