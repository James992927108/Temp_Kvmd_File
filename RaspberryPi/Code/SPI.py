import RPi.GPIO as GPIO 
import time

SPI_PIN = [19,21,23,24]

GPIO.setwarnings(False) 	#disable warnings
GPIO.setmode(GPIO.BOARD)

GPIO.setup(SPI_PIN, GPIO.OUT, initial=GPIO.HIGH)

GPIO.output(SPI_PIN, GPIO.HIGH)

# GPIO.cleanup()
# print("EATX Power off")
