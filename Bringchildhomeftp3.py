import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector 
import time
from difflib import SequenceMatcher
import urllib.parse
import urllib.request

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import smtplib, ssl

def sendEmail():
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "chinli2001123@gmail.com"
    receiver_email = "18086264@imail.sunway.edu.my"
    password = ("walaodiam123")
    message = """\
    Subject: You picked your children
    
    Is it u picked the child????????."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

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
    GPIO.setmode(GPIO.BCM)
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


def refresh(word,sid,parentName,timeNow):
# Raspberry Pi pin configuration:
    print("begun")
    RST = None     # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0
    
    # Beaglebone Black pin configuration:
    # RST = 'P9_12'
    # Note the following are only used with SPI:
    # DC = 'P9_15'
    # SPI_PORT = 1
    # SPI_DEVICE = 0

    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # 128x64 display with hardware I2C:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

    # Note you can change the I2C address by passing an i2c_address parameter like:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

    # Alternatively you can specify an explicit I2C bus number, for example
    # with the 128x32 display you would use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

    # 128x32 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # 128x64 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # Alternatively you can specify a software SPI implementation by providing
    # digital GPIO pin numbers for all the required display pins.  For example
    # on a Raspberry Pi with the 128x32 display you might use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

    # Initialize library.
    disp.begin()
    print("begun")
    # Clear display.
    disp.clear()
    disp.display()
    print("display")


    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0


    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)


    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.

    draw.text((x, top),        str(word),  font=font, fill=255)
    draw.text((x, top+8),    str(sid), font=font, fill=255)
    draw.text((x, top+16),     str(parentName),  font=font, fill=255)
    draw.text((x, top+25),     str(timeNow),  font=font, fill=255)


# Display image.
    disp.image(image)
    disp.display()
refresh("1","2","3","4")
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


mydb = mysql.connector.connect(
  host="localhost",
  user="mydb",
  passwd="password",
  database="hydro"

)
mycursor = mydb.cursor()


def autentication(ScannedCard):
    url = 'http://boitanpow.000webhostapp.com/myhtp.php'
    values = {'autentication': '',
              'ScannedCard': ScannedCard,
               }

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()
    mylist = the_page.decode().split(",")
    return mylist
print(autentication("943343799769"))

def getCard2id():
    print("Please autenticated your second card")
    refresh("----","Please autenticated your","second card","----")

    ledLightOnOrange()
    time.sleep(3)
    id, text2 = reader.read()
    mySecCard = text2
    mySecCardId = id
    return mySecCardId

reader = SimpleMFRC522()


try:
        while True:
                 
                    #store the list of card to check
                    print("Scan your first card to bring your child home")
                    refresh("---","Scan your card to bring","your children home","----")
                    id1, text = reader.read()
                    #get the id and name of the card
                    #print(id)
                    #print(text)
                    #print("Num of time :",counter)
                    # print how many time it scan
                    
                    #do a validation that cannot scan the card twice
                    #can be done by forcing all the 4 column to be the diffrent value or comparison with the value that previosly inserted
                    
                    myFirstCard = text
                    myFirstCardId = id1
                    returnedAutentication = (autentication(myFirstCardId))#)#+"is the resultttt")
                    autenList = str(returnedAutentication).replace("'", "")
                    newAuten = str(autenList).split(',')
                    newA = [x.strip(' [ ] ') for x in newAuten]
                    #print(newA[0],"index 0 ")
                    print(newA)
                    print()
                    #print(newA[1],"index 1 ")

                    print(myFirstCardId)
                    print()
                    if newA.__contains__(str(myFirstCardId)):
                        print("Card is in the autentication")
                        print(str(myFirstCardId))
                        refresh(str(myFirstCardId),str(myFirstCardId),str(myFirstCardId),str(myFirstCardId))
                        index = newA.index(str(myFirstCardId))
                        #if the index is equal 0 mean first item from the query then its parent so i nid to compare with index 2
                        if index == 0 :
                            print("parent just scan the card\n")
                            
                            Card2id = getCard2id()
                            print(str(Card2id))
                            refresh("Parent Just","Scan the card","--Student please scan--",str(Card2id))
                            #print(Card2id,"card2")
                           # print(newA[1],"new a [1]")
                            if str(Card2id) == newA[1]:
                                #if Card2 that is same as the newA[1] which is the index that return in the sql query
                                #student are passed
                                print("**Parent and student are matched**\n")
                                refresh("Parent and student","are matched",str(myFirstCardId),str(Card2id))

                            elif str(Card2id) == newA[0]:
                                #if the parent scan the card twice
                                #because newA[0] is the parent card already
                                print("**Parent cannot scan the card twice\nPlease scan again**")
                                refresh("Parent cannot scan","the card twice","Please scan again",str(Card2id))
   
                            else:
                                print("**Parent and student are not matched**\n")
                                refresh("Parent and student ","are not matched","Please scan again",str(Card2id))


                        else:
                            print("student just scan the card\n")
                            refresh("----","student just ","Scaned the card","----")
                            ledLightOnRed()

                            Card2id = getCard2id()
                            if str(Card2id) == newA[0]:
                 
                                print("**student and parent are matched**\n")
                                refresh("Parent and student","are matched",str(myFirstCardId),str(Card2id))
                                ledLightOnGreen()
                                sendEmail()

                            elif str(Card2id) == newA[1]:
                                refresh("student cannot scan","the card twice","Please scan again",str(Card2id))
                                ledLightOnRed()

                            else:
                                refresh("student cannot ","the card twice","Please scan again",str(Card2id))

                        time.sleep(3)
                    elif newA[0]== "":
                        #if newA return nothing mean no record in database
                        print("Card is not registered yet\n")
                        time.sleep(3)

                    else:
                        print("Card not in the autentication\n")
                        #if the scanned card is not mathing the both record in the list
                        #means the card is registered but it doesnt math the record
                        time.sleep(3)
except Exception as e:
    print(e)
finally:
        GPIO.cleanup()

