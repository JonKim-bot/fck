import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from urllib import request, parse
from urllib.request import Request, urlopen
import subprocess
import smtplib, ssl
import time

#import datetime
from mysql.connector import Error

def refresh(word, sid, parentName, timeNow):
    # Raspberry Pi pin configuration:
    RST = None  # on the PiOLED this pin isnt used
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
    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)

    # Write two lines of text.

    draw.text((x, top), str(word), font=font, fill=255)
    draw.text((x, top + 8), str(sid), font=font, fill=255)
    draw.text((x, top + 16), str(parentName), font=font, fill=255)
    draw.text((x, top + 25), str(timeNow), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()



refresh("1", "2", "3", "4")
reader = SimpleMFRC522()

def connectSql():
    conn = mysql.connector.connect(
        host="194.59.164.64",
        user="u615769276_boitan",
        passwd="password",
        database="u615769276_finalyear"
    )
    return conn
conn = connectSql()

def checkCardExistStudent(scannedCard):

    conn = connectSql()
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentId FROM studentTable WHERE studentId = '%s'""" % (
        str(scannedCard))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            return True
        else:
            return False
    except Error as error:
        print(error)

    finally:
        cursor.close()
def checkCardExistParent(scannedCard):

    conn = connectSql()
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentId FROM parentTable WHERE parentId = '%s'""" % (
        str(scannedCard))
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]

        # print(len(result),"num row")
        if len(result) > 0:
            return True
        else:
            return False
    except Error as error:
        print(error)

    finally:
        cursor.close()
def registerStudentCard(studentId,studentName):
    conn = connectSql()

    cursor = conn.cursor(prepared=True)
    try:
        
        if (checkCardExistStudent(studentId) == False) and (checkCardExistParent(studentId) == False):
            # if studentcard never register yet
            sql_insert_query = """INSERT INTO studentTable (studentId,studentName,studentCardStatus) VALUES (%s,%s,%s)"""

            insert_tuple = (studentId,studentName,"Invalid")
            

            cursor.execute(sql_insert_query, insert_tuple)
            conn.commit()
            refresh("--------------------", "Student Card", "Register Successfully", "----------------------")

            print("Data register student table using the prepared statement")
            time.sleep(2)
        else:
            print("Student Card Registered")
            refresh("--------------------", "This card ", "already registered", "----------------------")
            time.sleep(2)


    except mysql.connector.Error as error:
        print("student table parameterized query failed {}".format(error))
    finally:
        cursor.close()
def registerParentCard(parentId,parentName):
    conn = connectSql()

    cursor = conn.cursor(prepared=True)
    try:
        
        if (checkCardExistParent(parentId) == False) and (checkCardExistStudent(parentId) == False):
            # if studentcard never register yet
            sql_insert_query = """INSERT INTO parentTable (parentId,parentName,parentCardStatus) VALUES (%s,%s,%s)"""

            insert_tuple = (parentId,parentName,"Valid")
            

            cursor.execute(sql_insert_query, insert_tuple)
            conn.commit()
            refresh("--------------------", "Parent Card", "Register Successfully", "----------------------")
            time.sleep(2)

            print("Data register parent table using the prepared statement")
        else:
            print("parent Card Registered")
            refresh("----------------------", "This card ", "already registered", "----------------------")
            time.sleep(2)


    except mysql.connector.Error as error:
        print("student table parameterized query failed {}".format(error))
    finally:
        cursor.close()
def registerParent():
    try:
        refresh("--------------------", "Register Parent", "Input Parent Name", "----------------------")

        text = input("Parent Name : ")
        print("Place card to write")
        reader.write(text)
        refresh("----------------------", "Reading Card", "Please Wait", "----------------------")

        print("written parentName")
        id, text = reader.read()

        print(id)
        print(text)
        registerParentCard(id,text)
    except Exception as e:
        print(e)
        print("Error occur, please try again")
    finally:
        GPIO.cleanup()
        
def registerStudent():
    try:
        refresh("--------------------", "Register student", "Input student Name", "----------------------")

        text = input("Student Name : ")
        print("Place card to write")
        reader.write(text)
        refresh("----------------------", "Reading Card", "Please Wait", "----------------------")

        print("written studentTable")
        id, text = reader.read()
        print(id)
        print(text)
        registerStudentCard(id,text)
    except Exception as e:
        print(e)
        print("Error occur, please try again")
    finally:
        GPIO.cleanup()
while True:
    refresh("Select register people", "1 - Parent", "2 - Student ", "----------------------")

    getUserInput = input("Select register people\n1-Parent\n2-Student\n:")
    if (int(getUserInput) == 1):
        registerParent()
    elif(int(getUserInput) == 2):
        registerStudent()
    else:
        print("Invalid Selection")
        refresh("----------------------", "Invalid", "Selection", "----------------------")


        