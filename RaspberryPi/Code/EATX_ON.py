import RPi.GPIO as GPIO

EATX_PWR_PIN = 11

GPIO.setwarnings(False)     #disable warnings
GPIO.setmode(GPIO.BOARD)

GPIO.setup(EATX_PWR_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(EATX_PWR_PIN, GPIO.HIGH)

print("EATX Power on")