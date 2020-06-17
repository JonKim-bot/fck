import RPi.GPIO as GPIO
buzzer = 24
import time

def buzzerOn():
    GPIO.setwarnings(False)
    #Select GPIO mode
    GPIO.setmode(GPIO.BCM)
    #Set buzzer - pin 23 as output
    
    GPIO.setup(buzzer,GPIO.OUT)
    
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.2) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    GPIO.cleanup()  # Clean up
buzzerOn()