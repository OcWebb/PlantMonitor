import RPi.GPIO as GPIO
from app_package import db
from app_package.models import Reading

import board
from time import sleep

delay = .2
samples = 15


while True:
    try:
        temp_totaled = 0;
        humidity_totaled = 0;

        for i in range(samples):
            temperature_f = dhtDevice.temperature * (9 / 5) + 32
            humidity = dhtDevice.humidity

            temp_totaled = temp_totaled + temperature_f
            humidity_totaled = humidity_totaled + humidity

            print("Temp: {:.1f} F    Humidity: {}".format(temperature_f, humidity))
            sleep(delay)

        avg_temp = temp_totaled/samples
        avg_humidity = humidity_totaled/samples
        print("\nAVERAGE\nTemp: {:.1f} F    Humidity: {}%\n".format(avg_temp, avg_humidity))
        
        data = Reading(temperature=avg_temp, humidity=avg_humidity)
        db.session.add(data)
        db.session.commit()

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        sleep(delay)
        continue

    except Exception as error:
        dhtDevice.exit()
        raise error

    

    sleep(delay)




