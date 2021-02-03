import RPi.GPIO as GPIO
import time

EATX_PWR_PIN = 11
GPIO.setwarnings(False)     #disable warnings
GPIO.setmode(GPIO.BOARD)

GPIO.setup(EATX_PWR_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(EATX_PWR_PIN, GPIO.HIGH)
GPIO.cleanup()
print("EATX Power off")
