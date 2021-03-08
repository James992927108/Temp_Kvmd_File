import RPi.GPIO as GPIO
import time

PWR_PIN = 13

GPIO.setwarnings(False)     #disable warnings
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PWR_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(PWR_PIN, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(PWR_PIN, GPIO.LOW)

print("MotherBoard Power on")