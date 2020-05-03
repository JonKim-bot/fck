import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
#import bringChildhomerealsql 
#import NewestCheckInCheckOut 
def ledLightOnGreen():
    print ("LED Green On")

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)

    GPIO.output(21,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(16,GPIO.OUT)
    print ("LED on")
    GPIO.output(16,GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup() # Clean up

def ledLightOnRed():
    print ("LED Red On")
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(21,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    print ("LED on")
    GPIO.output(18,GPIO.HIGH)
    time.sleep(5)

    GPIO.cleanup() # Clean up

def ledLightOnOrange():
    print ("LED Orange On")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(21,GPIO.OUT)
    print ("LED on")
    GPIO.output(21,GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup() # Clean up
def button_callback(channel):
    print("Button was pushed!")
    #GPIO.cleanup() # Clean up
#import bringChildhomerealsql 

   # ledLightOnGreen()
    #main()
def button_callback2(channel):
    print("Button2 was pushed!")
#GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(18,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
 # Setup event on pin 10 rising edge
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(16,GPIO.RISING,callback=button_callback2) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n")

# Run until someone presses enter
GPIO.cleanup() # Clean up

#main()