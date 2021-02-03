import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
# Pause right here and check GPIO pin 21 is high (3.3 V)
GPIO.output(21, GPIO.HIGH)
GPIO.output(21, GPIO.LOW)
GPIO.cleanup()
quit()