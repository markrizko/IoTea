import time
import RPi.GPIO as GPIO
from datetime import datetime
from pythonping import ping
import pytz

# initialize time zone
tz_LA = pytz.timezone('America/Los_Angeles')


# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
# starts off HIGH = open circuit
GPIO.output(17, GPIO.HIGH)

signal = False # signal bool


while True: # system operational
    dt_LA = datetime.now(tz_LA) # initialize time
    # if out of range sleep and check every five minutes
    if (dt_LA.hour < 9) or (dt_LA.hour > 11):
        time.sleep(300)
    else:
        # pi is not sleeping, awaiting signal
        resp = ping('192.168.1.46')
        # if ping, set signal to true
        for re in resp:
            if re.success == True:
                signal = True
        if signal:
            # set it false for next time since it only fires once
            signal = False
            GPIO.output(GPIO.LOW) # activate kettle
            time.sleep(300) # wait 5 minutes for kettle to finish
            GPIO.output(GPIO.HIGH) # open circuit
            
            dt_LA = datetime.now(tz_LA)
            # check every minute until it's the hour mark, then go back to sleep until out of range (2 hours)
            while dt_LA.minute != 0:
                time.sleep(58) # check every 58 seconds
                dt_LA = datetime.now(tz_LA)
                if dt_LA.minute == 0:
                    time.sleep(7200) # 2 hours takes us out of range and keeps us close to the hour mark
