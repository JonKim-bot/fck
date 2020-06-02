import cv2
import os
import tkinter
from tkinter import *
from PIL import Image
import RPi.GPIO as GPIO
import sys
from PIL import ImageTk
from mysql.connector import Error
import mysql.connector
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tkinter import filedialog
import cv2
import tkinter.messagebox
import pyqrcode
from pyzbar.pyzbar import  decode
from PIL import Image
from urllib import request, parse
from urllib.request import Request, urlopen
from datetime import datetime
from datetime import date
import smtplib, ssl
import subprocess
import time

def connectSql():
    conn = mysql.connector.connect(
        host="194.59.164.64",
        user="u615769276_boitan",
        passwd="password",
        database="u615769276_finalyear"
    )
    return conn



def ledLightOnGreen():
    print("LED Green On")


    GPIO.setmode(GPIO.BCM)

    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(21, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(16, GPIO.OUT)
    print("LED on")
    GPIO.output(16, GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup()  # Clean up


def ledLightOnRed():
    print("LED Red On")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print("LED on")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(5)

    GPIO.cleanup()  # Clean up


def ledLightOnOrange():
    print("LED Orange On")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)
    print("LED on")
    GPIO.output(21, GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup()  # Clean up


def sendEmail(email):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "chinli2001123@gmail.com"
    receiver_email = email
    password = ("Caonima123=")
    message = """\
    Subject: qr code pick up your children
    Is it u picked the child????????."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def getEmail(pCardId):
    conn = connectSql()
    print(pCardId)
    query = """SELECT email FROM parentTable WHERE parentId = '%s'""" % (
        str(pCardId))
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
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return 0
    except Error as error:
        print(error)

    finally:
        cursor.close()


def getParentId(studentName, pickUpDate, pickUpTimeOne, pickUpTimeTwo):
    # check wherther the card punch card today or not if return any row then yes
    conn = connectSql()
    print(studentName)
    print(pickUpDate)
    print(pickUpTimeOne)
    print(pickUpTimeTwo)
    print("--------------------------")

    query = """SELECT parentId FROM tblParentBooking WHERE studentName = '%s' AND pickUpTimeOne = '%s' AND pickUpTimeTwo = '%s' AND pickUpDate = '%s'""" % (
        str(studentName), pickUpTimeOne, pickUpTimeTwo, pickUpDate)
    cursor = conn.cursor(buffered=True)

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]
        print(final_result, "is parentid")
        print(result, "is parentid")

        # print(len(result),"num row")
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return 0
    except Error as error:
        print(error)

    finally:
        cursor.close()


def updateBooking(bookingId):
    conn = connectSql()
    cursor = conn.cursor(prepared=True)
    try:

        sql_update_query = """UPDATE tblParentBooking SET status=%s WHERE bookingId=%s"""
        status = "used"
        print(status, bookingId, "is status and booking")
        data_tuple = (status, bookingId)

        cursor.execute(sql_update_query, data_tuple)
        conn.commit()
        return "Booking Update Success"
    except mysql.connector.Error as error:
        return ("updateCheckOut parameterized query failed {}".format(error))
    finally:
        cursor.close()


def validStudent(sCardId, dateToday, type1):
    # check wherther the card punch card today or not if return any row then yes
    conn = connectSql()
    query = """SELECT studentId FROM tblNotifications WHERE studentId = '%s' AND msgDate = '%s' AND type='%s'""" % (
        str(sCardId), dateToday, type1)
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
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return len(result)
        else:
            return 0
    except Error as error:
        print(error)

    finally:
        cursor.close()


def insertQr(parentId, parentName, studentId, type, status, message, checkInOutTime, msgDate,
             confirmStatus):
    conn = connectSql()
    cursor = conn.cursor(prepared=True)
    try:

        sql_insert_query = """INSERT INTO tblNotifications (parentId,parentName,studentId,type,status,message,checkInOutTime,msgDate,confirmStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        print(parentId)
        print(parentName)
        print(studentId)
        print(type)
        print(status)
        print(message)
        print(checkInOutTime)
        print(msgDate)
        print(confirmStatus)
        insert_tuple = (
            parentId, parentName, studentId, type, status, message, checkInOutTime, msgDate, confirmStatus)
        cursor.execute(sql_insert_query, insert_tuple)
        conn.commit()

        return "Insert Qr PickUp Success"

    except mysql.connector.Error as error:
        return "attendance table parameterized query failed {}".format(error)

    finally:
        cursor.close()

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


def insertQrPickUp(updateId, pickUpDate, timeNow):
    # check booking data by passing all data inhere
    # check booking data by passing all data inhere
    conn = connectSql()
    cursor = conn.cursor(buffered=True)

    query = """SELECT * FROM tblParentBooking WHERE bookingId='%s'""" % (
        (updateId))

    try:
        # extablish the connection again
        # pass in the query and the argurment
        # pass in the query and the argurment

        cursor.execute(query)
        conn.commit()
        result = list(cursor.fetchall())
        final_result = [list(i) for i in result]
        print(final_result)
        # print(len(result),"num row")
        if len(result) > 0:
            data = ''
            parentId = final_result[0][1]
            parentName = final_result[0][3]
            studentId = final_result[0][2]
            studentName = final_result[0][4]
            type = "qrPickUp"
            status = "unread"
            numOfResult1 = int(validStudent(studentId, pickUpDate, "qrPickUp"))
            numOfResult2 = int(validStudent(studentId, pickUpDate, "pickUp"))
            Msg = "Dear " + str(parentName) + "Your Child " + str(studentName) + "got qr pick up at " + str(
                timeNow)
            confirmStatus = "0"

            if (numOfResult1 < 1 and numOfResult2 < 1):
                qrPickUpStatus = insertQr(parentId, parentName, studentId, type, status, Msg, timeNow,
                                          pickUpDate, confirmStatus)
                # get index of parentId Column
                return qrPickUpStatus


            else:
                return 'Student go back already today without qr'
        else:
            data = "None"
            return data
    except Error as error:
        print(error)

    finally:
        cursor.close()


def checkBooking(studentName, pickUpDate, pickUpTimeOne, pickUpTimeTwo, todayTime):
    # check booking data by passing all data inhere
    # check booking data by passing all data inhere
    TimeNow = (datetime.now().strftime("%H:%M"))
    today = date.today()
    print(today, " is today")
    print(pickUpDate, "pick up date")
    try:


        if (str(today) == str(pickUpDate)):
            # if time are today then
            if (isNowInTimePeriod(pickUpTimeOne, pickUpTimeTwo, TimeNow)) == True:
                # if time are with in the range then request
                # extablish the connection again
                # pass in the query and the argurment
                # pass in the query and the argurment
                conn = connectSql()
                cursor = conn.cursor(buffered=True)

                query = """SELECT * FROM tblParentBooking WHERE studentName='%s' AND pickUpDate='%s' AND pickUpTimeOne='%s' AND pickUpTimeTwo='%s' AND status='unuse'""" % (
                    (studentName, pickUpDate, pickUpTimeOne, pickUpTimeTwo))

                cursor.execute(query)
                conn.commit()
                result = list(cursor.fetchall())
                final_result = [list(i) for i in result]
                print(final_result, "is the result")
                finalData = ''
                print(len(final_result), "num row")
                if len(result) > 0:
                    updateId = final_result[0][0]
                    print(pickUpDate)
                    insertQrPickUpId = insertQrPickUp(updateId, pickUpDate, todayTime)
                    print(insertQrPickUpId, "is pick up status")

                    if insertQrPickUpId == "Insert Qr PickUp Success":
                        updateStatus = updateBooking(updateId)
                        print(updateStatus)

                        if (updateStatus == "Booking Update Success"):
                            finalData = "Valid"
                        else:
                            finalData = "Not Valid"

                    else:
                        finalData = "Not Valid"
                else:
                    finalData = "Not Valid"
                print(finalData)

                if finalData == "Valid":
                    ledLightOnGreen()


                    refresh("-----------------", "Valid Qr Code", studentName, "--------------------")
                    parentId = getParentId(studentName, pickUpDate, pickUpTimeOne, pickUpTimeTwo)
                    # get parent id from tblparentbooking
                    print(parentId)
                    parentEmail = getEmail(parentId)
                    # get email by passing the parent id
                    print("parent email", parentEmail)
                    sendEmail(parentEmail)
                    # send confirm email
                    print("can bring children home")
                    tkinter.messagebox.showinfo(title="Valid Qr Code", message="can bring children home")

                elif finalData == "Not Valid":
                    refresh("-----------------", "qr code expired ", "not able to use", "--------------------")

                    ledLightOnRed()
                    print("qr code expired")
                    tkinter.messagebox.showinfo(title="Qr Code Not Valid", message="qr code expired")

                elif finalData == "No Record Found":
                    refresh("-----------------", "No booking found ", "qr code expired", "--------------------")
                    ledLightOnRed()

                    tkinter.messagebox.showwarning(title="No Booking Record Found",
                                                  message="No Booking Record Found , Please make the booking first.")

                    print("No Booking Record Found , Please make the booking first.")
            else:
                refresh("----------------------", "Time not reach yet", "--------------------------", "--------------------")
                ledLightOnRed()

                tkinter.messagebox.showwarning(title="Time Not Reached Yet",
                                               message="Time Now Are Not With in the range")

                print("Booking Time Not With In The Range")
        else:
            

            print("Booking Date are not today!")
            ledLightOnRed()
            refresh("----------------------", "Qr code booking date", "Are not today", "--------------------")
            tkinter.messagebox.showwarning(title="Booking Date are not today",
                                           message="Booking Date are not today,please try again with another qr code")

    except Error as error:
        refresh("-----------------", "qr code expired ", "not able to use", "--------------------")

        print(error)
        ledLightOnRed()

   # finally:
      #  cap.release()
     #   cv2.destroyAllWindows()
        # get the currrent time in hour and minit format


def isNowInTimePeriod(startTime, endTime, nowTime):
    # check if the time are with in the range , if not then cannot use qrcode
    if startTime < nowTime and nowTime < endTime:
        return True
    else:
        return False

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

detector = cv2.QRCodeDetector()

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)

    if (bbox is not None):
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255,
                                                                                         0, 255), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if data:
            print("data found: ", data)
            try:
                refresh("----------------------", "Please wait.....", "Reading Qr Code", "--------------------")

                qrcodeArr = data.split(",")
                print(qrcodeArr[0])
                print(qrcodeArr[1])
                print(qrcodeArr[2])
                print(qrcodeArr[3])
                TimeNow = (datetime.now().strftime("%H:%M"))
                todayTime = datetime.now().time()
                print(todayTime)
                checkBooking(qrcodeArr[0], qrcodeArr[1], qrcodeArr[2], qrcodeArr[3], todayTime)
                sys.exit()

            except Exception as e:
                print(e)

          #      cap.release()
           #     cv2.destroyAllWindows()
                ledLightOnRed()

                refresh("------------------------", "Invalid QR Code", "Use another Qr code", "---------------------------")

                tkinter.messagebox.showwarning(title="Error",
                                               message="Invalid Qr Code\nPlease use qr code for booking")
                sys.exit()

    cv2.imshow("code detector", img)
    if (cv2.waitKey(1) == ord("q")):
        break
cap.release()
cv2.destroyAllWindows()