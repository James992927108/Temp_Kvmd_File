import RPi.GPIO as GPIO 
import time

EATX_PWR_PIN = 11
GPIO.setwarnings(False) 	#disable warnings
GPIO.setmode(GPIO.BOARD)

GPIO.setup(EATX_PWR_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(EATX_PWR_PIN, GPIO.LOW)
print("EATX Power on")

# time.sleep(1)

# PWR_PIN = 18
# GPIO.setup(PWR_PIN, GPIO.OUT, initial=GPIO.LOW)
# GPIO.output(PWR_PIN, GPIO.HIGH)
# time.sleep(0.5)
# GPIO.output(PWR_PIN, GPIO.LOW)

# print("MotherBoard Power on")