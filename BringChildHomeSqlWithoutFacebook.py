#!/usr/bin/python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import time

from difflib import SequenceMatcher
import urllib.parse
# import datetime
import buzzer

from mysql.connector import Error

import urllib.request
import datetime
from fbchat import Client, ThreadType, Message

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from urllib import request, parse
from urllib.request import Request, urlopen
import subprocess
import smtplib, ssl
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
client = Client()

print("Pick up module ... Booting....")
def sendNotifications(parentId,message):
    url = "https://boitan.000webhostapp.com/sendNotification.php"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    try:          # allStudent = []
              # values = {
              #         'allStudrecord' : "1",
              # }
              # data = urllib.parse.urlencode((values))
              # data = data.encode(('ascii'))
              # req = urllib.request.Request(url, data)
              # #response = request.urlopen(req)
              # with urllib.request.urlopen(req) as response:
              #         the_page = response.read()
              # allStudent = the_page.decode().split(",")
              # for x in allStudent:
              #         print(x)
              # print(i)
            data = {
                    'sendbyid': "1",
                'message': message,
                'parentId': parentId,

                #                'studentId': "943343799769",
                    #'studentId' : "943343799769",
                    #'parentId':'867364651663',
                    #'timeNow':'22',
                    #'datetoday': '2020-04-18'
      #              'timeNow' : now,
     #               'datetoday':datetime.now().strftime("%Y-%m-%d")
                    # 'boitan',"1"
                    }
            data = parse.urlencode(data).encode()

            req = Request(
                    url,
                    headers={'User-Agent': user_agent,
                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                             'Accept-Encoding': 'none',
                             'Accept-Language': 'en-US,en;q=0.8',
                             'Connection': 'keep-alive'
                             }
                    ,data=data)
            webpage = urlopen(req).read().decode()
            print(webpage)

    except Exception as e:
        print(e)

def sendEmail(email,studentName,todayDate,timeToday):

    msg = MIMEMultipart()
    msg['From'] = "boitan@piegensoftware.com"
    msg['To'] = email
    msg['Subject'] = 'RFID Tag Pick Up'
    message = 'Your kid ' +str(studentName) + "\nGet picked up today at the date of "+str(todayDate)+ " "+ str(timeToday) +"\n\nThanks,\nThe Piegen team"

    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.hostinger.my', 587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('boitan@piegensoftware.com', 'password')

    mailserver.sendmail('boitan@piegensoftware.com', email, msg.as_string())
    print("Email Sended,,,")
    mailserver.quit()
    
def ledLightOnGreen():
    print("LED Green On")

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(21, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

    GPIO.setwarnings(False)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    time.sleep(1.5)
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
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1.5)

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
    GPIO.output(21, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.cleanup()  # Clean up
ledLightOnGreen()

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
    print("Start Diplaying....")

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


refresh("------------------------------", "Pick up module", "Booting......", "----------------------------")


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def connectSql():
    conn = mysql.connector.connect(
        host="194.59.164.64",
        user="u615769276_boitan",
        passwd="password",
        database="u615769276_finalyear"
    )
    return conn


# cursor.execute("SELECT * FROM tblCard")
# result = cursor.fetchall()
# print(result)
global conn
conn = connectSql()
print(conn)

# NEW REMARK HERE !!!!!!!!!!!!!
def validStudent(studentId, dateToday, type,conn):
    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentId FROM tblNotifications WHERE studentId = '%s' AND msgDate = '%s' and type = '%s'""" % (
        str(studentId), str(dateToday), str(type))
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


def getStudentName(studentId,conn):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentName FROM studentTable WHERE studentId = '%s'""" % (
        str(studentId))
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
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()

def getParentId(studentId,conn):
    cursor = conn.cursor(buffered=True)


    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentId FROM studentTable WHERE studentId = '%s'""" % (
        str(studentId))

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
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()



def getParentName(studentId,conn):

    attendanceList = []
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentName FROM tblCard WHERE studentId = '%s'""" % (
        str(studentId))
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
            return "0"
    except Error as error:
        print(error)

    finally:
        cursor.close()


def autentication(ScannedCard,conn):
    attendanceList = []

    # check parent and student card id , return it in a array form
    query = """SELECT parentId,studentId FROM tblCard WHERE studentId='%s' AND studentId IS NOT NULL""" % (
        str(ScannedCard))
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
            return final_result[0]
        else:
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


# print(autentication("943343799769"))

def getCard2idRemix():
    print("Please autenticated your second card")
    refresh("----", "Please autenticated your", "second card", "----")

    ledLightOnOrange()
    time.sleep(3)

    id, text2 = reader.read()
    refresh("----------------", "PLEASE WAIT", "READING CARD", "---------------")

    mySecCard = text2
    mySecCardId = id
    return mySecCardId


def checkStudentCardStatus(sCardId,conn):

    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT studentCardStatus FROM studentTable WHERE studentId = '%s'""" % (
        str(sCardId))
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
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()
        
        
        
        


def checkParentCardStatus(pCardId,conn):

    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentCardStatus FROM parentTable WHERE parentId = '%s'""" % (
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
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


def insertPickUp(sCardId, pCardId, timeNow, dateToday,conn):

    cursor = conn.cursor(prepared=True)
    try:
        parentName = getParentName(sCardId,conn)
        studentName = getStudentName(sCardId,conn)
        parentId = (pCardId)

        message = "Dear " + str(parentName) + ", Your Child " + str(studentName) + " got pick up at " + str(timeNow)
        numOfResult = validStudent(sCardId, dateToday, "pickUp",conn)
        numOfResult2 = validStudent(sCardId, dateToday, "qrPickUp",conn)
        totalResult = int(numOfResult) + int(numOfResult2)
        confirmStatus = "0"
        type = "pickUp"
        status = "unread"
        if int(totalResult) < 1:
            # if student check in twice then cannot liao
            sql_insert_query = """INSERT INTO tblNotifications (parentId,parentName,studentId,type,status,message,checkInOutTime,msgDate,confirmStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            insert_tuple = (parentId, parentName, sCardId, type, status, message, timeNow, dateToday, confirmStatus)

            cursor.execute(sql_insert_query, insert_tuple)
            conn.commit()
            print("Data inserted successfully into pick up table using the prepared statement")
        else:
            print("student go back already today")

    except mysql.connector.Error as error:
        print("tblNotification table parameterized query failed {}".format(error))
    finally:
        cursor.close()


def validPickUp(sCardId, dateToday, type,conn):
    # check wherther the card punch card today or not if return any row then yes

    query = """SELECT studentId FROM tblNotifications WHERE studentId = '%s' AND msgDate = '%s' AND type='%s'""" % (
        str(sCardId), dateToday, type)
    cursor = conn.cursor(buffered=True)

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

        return len(result)

    except Error as error:
        print(error)

    finally:
        cursor.close()



def getEmail(pCardId,conn):

    query = """SELECT email FROM parentTable WHERE parentId = '%s'""" % (
        str(pCardId))
    cursor = conn.cursor(buffered=True)

    try:

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
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


def getAttendance(studentid, datetoday,conn):

    query = """SELECT Attendance FROM Attendance WHERE StudentCardId = '%s' AND Datee = '%s'""" % (
        str(studentid), datetoday)
    cursor = conn.cursor(buffered=True)

    try:

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
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


def findFbId(parentCardId,conn):
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT parentFbId FROM parentTable WHERE parentId = '%s' AND parentFbId IS NOT NULL""" % (
        str(parentCardId))
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
            return "None"
    except Error as error:
        print(error)

    finally:
        cursor.close()


reader = SimpleMFRC522()


# def main():
def main():
  #  await client.start("0169787592", "jijiji123")
 #   print("****Login Success*****")
    print("Run with out facebook")

    def getCard2id():
        print("Parent autenticate their card....")
        refresh("---------------------------------", "Parent Please Scan", "Your Card", "---------------------------------")

        ledLightOnOrange()

        id, text2 = reader.read()
        print("Card ID : ",id)
        print("Card Holder Name : ",text2)

        buzzer.buzzerOn()
        conn = connectSql()



        refresh("---------------------------------", "PLEASE WAIT...", "READING CARD...", "---------------------------------")

        mySecCard = text2
        mySecCardId = id
        print("Parent Name :  " + str(mySecCard))
        return mySecCardId


    try:
        while True:
            conn = connectSql()

            # store the list of card to check
            print("Student scan the card..")
            refresh("---------------------------------", "Student Please Scan", "Your Card", "---------------------------------")
            id1, text = reader.read()

            buzzer.buzzerOn()
            ledLightOnRed()

            refresh("---------------------------------", "PLEASE WAIT...", "READING CARD....", "---------------------------------")
            conn = connectSql()
            print("Card ID : ",id1)
            print("Card Holder Name : ",text)

            # get the id and name of the card
            # print(id)
            # print(text)
            # print("Num of time :",counter)
            # print how many time it scan

            # do a validation that cannot scan the card twice
            # can be done by forcing all the 4 column to be the diffrent value or comparison with the value that previosly inserted

            myFirstCard = text
            
            
            myFirstCardId = id1
            returnedAutentication = (autentication(myFirstCardId,conn))  # )#+"is the resultttt")
            #print(returnedAutentication, " is returned autenticated")
            if (returnedAutentication != "None"):
                autenList = str(returnedAutentication).replace("'", "")
                newAuten = str(autenList).split(',')
                newA = [x.strip(' [ ] ') for x in newAuten]
            else:
                newA = ['None', 'None']

            #print(newA[0], "index 0 ")
            #print(newA)

            print()
           # print(newA[1], "index 1 ")
            today = datetime.date.today()

            print("Date Today : ",today)
            todaytime = datetime.datetime.now().time().replace(microsecond=0)
            print("Time Now : ",todaytime)

            #print(myFirstCardId)
            print()
            if newA.__contains__(str(myFirstCardId)):
                print("Card is in the autentication")
                #print(str(myFirstCardId))
                index = newA.index(str(myFirstCardId))
               # print(index, "is the new a indexx ohhhh")

                # valid pick up is string
                validPickUp2 = (int(validPickUp(myFirstCardId, today, "pickUp",conn))) + (
                    int(validPickUp(myFirstCardId, today, "qrPickUp",conn)))
                # valid pick up checking for index 1
                print(validPickUp2, " is the valid pick up")
                # if the index is equal 0 mean first item from the query then its parent so i nid to compare with index 2
                parentCardStatus = checkParentCardStatus(myFirstCardId,conn)
                studentCardStatus2 = checkStudentCardStatus(myFirstCardId,conn)
                # check student card status for index 1
                # to see if parent card are valid or not
                if index == 0 and parentCardStatus == "Valid":
                    print("parent just scan the card\n")
                    parentEmail = getEmail(myFirstCardId,conn)
                    parentFb = findFbId(myFirstCardId,conn)

                    # new a return the matching student id to be scanned
                    refresh("Parent Just", "Scan the card", "--Student please scan--", newA[1])
                    ledLightOnRed()
                    sendNotifications(myFirstCardId,"You are picking up your child")
                    Card2id = getCard2id()
                    # get the secound index to be scanned
                    print(str(Card2id))

                    print("parent scanned ")
                    studentCardStatus = checkStudentCardStatus(int(Card2id),conn)
                    # check student card status
                    checkPickUp = (int(validPickUp(Card2id, today, "pickUp",conn))) + (
                        int(validPickUp(Card2id, today, "qrPickUp",conn)))
                    # check if student picked up already or not
                    AttendanceStatus = getAttendance(Card2id, today,conn)
                    # print(Card2id,"card2")
                    # print(newA[1],"new a [1]")
                    
                    
                    if str(Card2id) == newA[1] and studentCardStatus == "Valid" and int(
                            checkPickUp) < 1 and AttendanceStatus == "present":
                        # if Card2 that is same as the newA[1] which is the index that return in the sql query
                        # student are passed
                        print("**Parent and student are matched**\n")
                        refresh("Parent and student", "are matched", str(myFirstCardId), str(Card2id))
                        insertPickUp(Card2id, myFirstCardId, todaytime, today,conn)
                        sendNotifications(myFirstCardId,"You picked up your child at " + str(todaytime))

                        ledLightOnGreen()
                       # if parentFb != "None":  # if the user really have fb id
                         #   user = (await client.search_for_users(parentFb))[0]
                          #  parentFbId = user.uid
                           # parentFbName = user.name

                            # store the parentFb id
                         #   await client.send(Message(
                         #       text="Dear " + str(parentFbName) + ", You picked up your child : " + str(
                      #              Card2id) + " at " + str(todaytime) + ", in the date of " + str(today)),
                       #         thread_id=int(parentFbId), thread_type=ThreadType.USER)
                        refresh("---------------------------------", "NOTIFICATIONS", "SUCCESSFULLY SENDED", "---------------------------------")
                      #  else:
                      #      refresh("---------------------------------", "PARENT FACEBOOK", "NOT FOUND", "---------------------------------")

                          #  print("parent fb not found")
                        sendEmail(parentEmail,myFirstCard,today,todaytime)
                        refresh("---------------------------------", "EMAIL SENDED", "CHECK YOUR EMAIL", "---------------------------------")

                        print(parentEmail, " is email 1 ")

                    elif str(Card2id) == newA[0]:
                        # if the parent scan the card twice
                        # because newA[0] is the parent card already
                        print("**Parent cannot scan the card twice\nPlease scan again**")
                        refresh("Parent cannot scan", "the card twice", "Please scan again", str(Card2id))
                        ledLightOnRed()

                    elif studentCardStatus != "Valid":
                        refresh("---------------------------------", "Student card Invalid", "Please contact admin", "---------------------------------")
                        ledLightOnRed()
                    elif int(checkPickUp) >= 1:
                        refresh("---------------------------------", "student card check in already", "Please scan again", "---------------------------------")

                        ledLightOnRed()
                    elif AttendanceStatus == "None":
                        refresh("---------------------------------", "Student Absents", "Didn Attend Today", "---------------------------------")
                        print("Student havent attend today")
                        ledLightOnRed()
                    else:
                        print("**Parent and student are not matched**\n")
                        refresh("-----------------------------------", "Autentication Failed", "ID Not Matched ",
                                "-----------------------------------")
                        ledLightOnRed()
                        ##may be can do a send notification fail to parent????


                elif index == 1 and studentCardStatus2 == "Valid" and int(validPickUp2) < 1:
                    print("Student just scan the card\n")
                    AttendanceStatus = getAttendance(myFirstCardId, today,conn)
                    if (AttendanceStatus == "present"):

                        refresh("---------------------------------", "Student ", "Scanned The Card", "---------------------------------")
                        ledLightOnRed()
                        print(myFirstCardId, "is student ")
                        
                        sendNotifications(getParentId(myFirstCardId,conn),"You are picking up your child " + str(myFirstCard))




                        Card2id = getCard2id()
                        cparentCardStatus = checkParentCardStatus(int(Card2id),conn)

                        if str(Card2id) == newA[0] and cparentCardStatus == "Valid":
                            parentEmail = getEmail(Card2id,conn)
                            print(parentEmail, " is email of the parent...")
                            parentFb = findFbId(Card2id,conn)

                            print("**Autentication success**\n")
                            print(Card2id, "is parent card id")
                            refresh("------------------------------", "Autentication Success", "ID Matches", "----------------------------")
                            insertPickUp(myFirstCardId, Card2id, todaytime, today,conn)

                            ledLightOnGreen()
                            #if parentFb != "None":  # if the user really have fb id
                             #   user = (await client.search_for_users(parentFb))[0]
                              #  parentFbId = user.uid
                               # parentFbName = user.name

                                # store the parentFb id
                                #await client.send(Message(
                                 #   text="Dear " + str(parentFbName) + ", You picked up your child : " + str(
                                  #      myFirstCard) + " at " + str(todaytime) + ", in the date of " + str(today)),
                                   # thread_id=int(parentFbId), thread_type=ThreadType.USER)
                            refresh("---------------------------------", "NOTIFICATIONS", "SUCCESSFULLY SENDED", "---------------------------------")
                           # else:
                               # refresh("---------------------------------", "PARENT FACEBOOK", "NOT FOUND", "---------------------------------")

                             #   print("Parent fb not found")
                            sendEmail(parentEmail,myFirstCard,today,todaytime)
                            sendNotifications((Card2id),"You picked up your child " + str(myFirstCard)+ " at " + str(todaytime))

                            refresh("---------------------------------", "EMAIL SENDED", "CHECK YOUR EMAIL", "---------------------------------")
                            print("Notification sended...")

                        elif str(Card2id) == newA[1]:
                            refresh("-----------------------------------","Duplicated Scanning","Please Try Again","------------------------------")
                            ledLightOnRed()
                            print("Duplicated scanning...")

                        elif cparentCardStatus != "Valid":
                            refresh("-----------------------------------", "Parent Card Invalid", "Please contact Admin", "-----------------------------------")
                            ledLightOnRed()
                            print("Parent Card Invalid..")


                        else:

                            print("Autentication failed")
                            refresh("-----------------------------------", "Autentication Failed", "ID Not Matched ", "-----------------------------------")
                            ledLightOnRed()
                    else:
                        refresh("---------------------------------", "Student Absents", "Didn Attend Today", "---------------------------------")
                        ledLightOnRed()
                        print("No attendance record found ")



                else:
                    if int(validPickUp2) >= 1:
                        # if student picked up already
                        refresh("--------------------------------", str(myFirstCard) + " Check Outed",
                                "Student go back already", "------------------------------")
                        ledLightOnRed()
                        print("Student go back already today...")
                    elif parentCardStatus != "Valid":

                        refresh("-----------------------------------", "Parent Card Invalid", "Please contact Admin",
                                "-----------------------------------")

                        ledLightOnRed()
                        print("Parent card invalid...")

                    elif studentCardStatus2 != "Valid":

                        refresh("-----------------------------------", "Student Card Invalid", "Please contact Admin",
                                "-----------------------------------")
                        ledLightOnRed()
                        print("Student card invalid...")

                    else:
                        print("Card invalid...")

                        refresh("-----------------------------------", "Card Invalid", "Please use registered Card",
                                "-----------------------------------")
                        ledLightOnRed()

                time.sleep(1)

            elif newA[0] == "":
                # if newA return nothing mean no record in database
                print("Card is not registered...\n")

                refresh("-----------------------------------", "Card Invalid", "Please use registered Card",
                        "-----------------------------------")
                ledLightOnRed()

            else:
                print("Card not in the autentication\n")
                ledLightOnRed()

                refresh("-----------------------------------", "Card Invalid", "Please use registered Card",
                        "-----------------------------------")
                # if the scanned card is not mathing the both record in the list
                # means the card is registered but it doesnt math the record
                ledLightOnRed()
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()

try:
    main()
except:
    print("Error occured please try again")

