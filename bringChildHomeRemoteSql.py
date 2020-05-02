import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import time
from difflib import SequenceMatcher
import datetime
import urllib.parse
import urllib.request
import json
from fbchat import Client, ThreadType, Message
from urllib import request, parse
from urllib.request import Request, urlopen
import subprocess
import smtplib, ssl
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
client = Client()

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
    print("Begin Display")
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
  host="194.59.164.64",
  user="u615769276_boitan",
  passwd="password",
  database="u615769276_finalyear"

)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM tblCard")
result = mycursor.fetchall()
print(result)

#
def checkAttendance(scardId,datetoday):
    attendanceList = []
    #check wherther the card punch card today or not if return any row then yes
    try:
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'scardId': scardId,
                  'datetoday': datetoday,
                  'checkAttendance': '' }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print("!!error")
        print(e)
#print(checkAttendance('943343799769',"2019-12-13"),"9s")

def checkCard(scardId,datetoday):
    #check wherther the card punch card today or not if return any row then yes
    try:
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'scardId': scardId,
                  'datetoday': datetoday,
                  'checkCard': '' }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print("!!error")
        print(e)
#print(checkCard('943343799769',"2019-12-123"),"is student check card")
def checkCardCheckin(scardId,datetoday):
    #check wherther the card punch card today or not if return any row then yes
    try:
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'scardId': scardId,
                  'datetoday': datetoday,
                  
                  'checkCardCheckIn': '' }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print("!!error")
        print(e)
#print(checkCardCheckin("943343799769","2019-12-19"),"is the result from the list")
#print(type(checkCardCheckin("943343799769","2019-12-19")),"is type")
#newstr = checkCardCheckin("943343799769","2019-12-19")
#if int(newstr) == 1 :
#    print("new str is 1")
#else:
##   print("neww")
def insertCheckinOut(CardId):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'insertCheckinOut': '',
                  'CardId': CardId,
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)

def insertCheckin(CardId,time,datetoday):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'insertCheckin': '',
                  'CardId': CardId,
                  'time': time,
                  'datetoday': datetoday,
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)
#undone part !!!!!!!!!!!!!!!!!
def validateCard(myCardid):
    try:
        #mycursor.execute("""SELECT StudentCardId FROM Attendance WHERE StudentCardId=%s """, ('94334379769','2019-12-13',))
        #mycursor.execute("""SELECT StudentCardId FROM Attendance""")
        mycursor.execute("""SELECT  FROM Attendance WHERE StudentCardId=%s AND Datee=%s""", (scardId,datetoday,))
        myresult = mycursor.fetchall()

        for x in myresult:
          print(x)

#        print("student already punch card today")
        return mycursor.rowcount
    except Exception as e:
        print("!!error")
        print(e)

def CheckIfNotNull(scardID,datetoday):
     try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'CheckIfNotNull': '',
                  'scardId': scardID,
                  'datetoday': datetoday,
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
     except Exception as e:
        print(e)
#print(CheckIfNotNull('943343799769','2019-12-14'),"is the check if not null")
#bl = CheckIfNotNull('943343799769','2019-12-14')
#if bl == "" or bl=="None":
 #   print("not record found in check out")
#else:
  #  print("record found")
#check wherther is null or not
def updateCheckOut(CardId,checkouttime):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'updateCheckOut': '',
                  'CardId': CardId,
                  'checkouttime': checkouttime,
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)
        
    
def insertStudentCheckin(CardId,datetoday):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'insertStudentCheckin': '',
                  'CardId': CardId,
                  'datetoday': datetoday,
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)
def insertCheckinNotification(sCardId,timeNow,datetoday):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'checkInNotification': '',
                  'studentId': sCardId,
                  'timeNow': timeNow,
                    'datetoday': datetoday,

                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)
def insertCheckoutNotification(sCardId,timeNow,datetoday):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'checkOutNotification': '',
                  'studentId': sCardId,
                  'timeNow': timeNow,
                    'datetoday': datetoday,

                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)
def findParentId(studentCardId):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'findParentId': '',
                  'studentId': studentCardId,
               

                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print(e)
def findFbId(parentCardId):
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'findFbId': '',
                  'parentId': parentCardId,
               

                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print(e)
def updateCheckin(CardId,checkInTime):
    try:
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'updateCheckIn': '',
                  'checkInTime': checkInTime,
                  'CardId': CardId,
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
    except Exception as e:
        print(e)
def allStudrecord():
    allStudent= []
    try:
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'allStudrecord': '',
                  
                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        print(webpage)
        allStudent = webpage.split(",")
        filter_object=filter(lambda x:x !="",allStudent)
        newAllStudent = list(filter_object)
        #remove empty list from all student
        return newAllStudent
    except Exception as e:
        print(e)
        
def checkStudentCardStatus(sCardId):
    #check student card valid or not
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'checkStudentCard': '',
                  'studentId': sCardId,
               

                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print(e)
def checkParentCardStatus(pCardId):
    #check parent card valid or not
    try:
        
        url = 'https://piegensoftware.com/myhtp.php'
        values = {'checkParentCard': '',
                  'parentId': pCardId,
               

                  }

        data = parse.urlencode(values).encode()
        req = Request(url,
            headers={'User-Agent': 'Mozilla/5.0'}
            ,data=data)
        webpage = urlopen(req).read().decode()
        return (webpage)
    except Exception as e:
        print(e)
    
#print(allStudrecord(),"is student record")
newStudentList = []


#print(CheckIfNotNull('943343799769','2019-12-19'),"is check if not null")
async def main():
    await client.start("0169787592", "nimabi123")    
    print("****Login Success*****")
    print(f"Own ID: {client.uid}")
    #await client.logout()
    #print(returnParentIds())
    reader = SimpleMFRC522()


    try:
            while True:
                        studentCardList = [943343799769]
                        parentCardList = [867364651663]
                        #store the list of card to check
                        
                        counter = 0
                        today = datetime.date.today()


                        for x in allStudrecord():
                            newStudentRecord = str(x).strip(",)`'(")
                        #print(newStudentRecord)#None after remove the extra character
                            newStudentList.append(newStudentRecord)#result = ['321', 'None', 'None', '943343799769']
                        try: 
                            for z in newStudentList:
                                #newStudentList return all the student card id in card table
                                if z != "None" and int(checkCard(z,today)) < 1:
                                    #if student id is not equal to none and check card today record is lest than one
                                    print("Havent punch card today",z)
                                    #then help that student to insert record
                                    insertStudentCheckin(z,today)
                                elif z != "None" and int(checkCard(z,today)) >= 1:
                                    print(z,"punch card already today!")
                        except:
                            print("***Something else when wrong***")
                            
                        #auto insertion of the record that have not punch car4d today
                        del newStudentList[:]
                        #clear the list or else it will duplicate
                        refresh("---","Scan your card to bring","record attendance","----")

                        print("Scan your Card to record attendance")
                        id1, text = reader.read()
                        refresh("---","reading card","recording attendance","----")

                        #get the id and name of the card

                                #print(id)
                        #print(text)
                        #print("Num of time :",counter)
                        # print how many time it scan
                        
                        #do a validation that cannot scan the card twice
                        #can be done by forcing all the 4 column to be the diffrent value or comparison with the value that previosly inserted
                        

                        myFirstCard = text
                        myCardId = id1#
                        today = datetime.date.today()
                        print(today)
                        todaytime = datetime.datetime.now().time()
                        print(todaytime)
                        studentCardStatus = checkStudentCardStatus(myCardId)
                        print(studentCardStatus,"is card status")
                        parentId = findParentId(myCardId)
                        #get the parent id by scanning student id
                        parentFb = findFbId(parentId)
                        #get the parent fb by passing parent id in

                        try:
                            if studentCardStatus == "Valid":
                                print("card valid")
                                checkCardIn = checkCardCheckin(myCardId,today)
                                checkAttend = checkAttendance(myCardId,today)
                                if checkCardIn == str(1) :
                                    #the checkCard check in return the row where
                    
                            #student already punch card but no check in record found
                                    #
                                    print("Havent punch card today")
                                    bl = CheckIfNotNull(myCardId,today)
                                    if bl == "" or bl == "None":
                                        #if the check in return null or havent check in yet
                         
                                        print("Student Havent check in yet")
                                        updateCheckin(myCardId,todaytime)
                                        insertCheckinNotification(myCardId,todaytime,today)
                                        refresh("-----------------","check in success","successfuly checked","----")

                                        #print(parentId ,"is parent id")

#get the parent id for search it in the email or fb
                                        if parentId !="None": #if the user really have fb id
                                            user =(await client.search_for_users(parentFb))[0]
                                            parentFbId = user.uid
                                            parentFbName = user.name

                                            #store the parentFb id
                                            await client.send(Message(text="Dear "+str(parentFbName)+", Your child : "+str(myFirstCard)+" checked in at "+str(todaytime) + ", in the date of, "+str(today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                            refresh("----------------","NOTIFICATIONS","SUCCESSFULLY SENDED","---------------")
                                        else:
                                            refresh("----------------","PARENT FACEBOOK","NOT FOUND","---------------")

                                            print("parent fb not found")

                                        time.sleep(3)
                                        #if the student already check in then update the check up
                                    else:
                                        #
                                        print("updating the checwwwwwk out")
                                        updateCheckOut(myCardId,todaytime)
                                        #get the parent id for search it in the email or fb
                                        if parentId !="None": #if the user really have fb id

                                            user =(await client.search_for_users(parentFb))[0]
                                            parentFbId = user.uid
                                            parentFbName = user.name

                                     #store the parentFb id
                                            await client.send(Message(text="Dear "+str(parentFbName)+", Your child : "+str(myFirstCard)+" checked in at "+str(todaytime)+ ", in the date of"+str(today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                        time.sleep(3)
                                        
                                elif checkAttend == "present":
                                    #add one more condition to check whether if he or she is present today
                                    print("punch card already today can go back ")
                                    refresh("---","punch card already","today can go back ","----")

                                    time.sleep(3)
                                    
                                
                                elif int(checkCard(myCardId,today)) >=1 and CheckIfNotNull(myCardId,today) != "None":

                                    #if the check in is not null and already insert today but the card 
                                    #print("punch check in already")
                                    print("updating the check out")
                                    
                                    updateCheckOut(myCardId,todaytime)
                                    insertCheckoutNotification(myCardId,todaytime,today)
                                    refresh("---","student check out ","checking out ","----")


                                    if parentId !="None": #if the user really have fb id
           #get the parent id for search it in the email or fb
                                        user =(await client.search_for_users(parentFb))[0]
                                        parentFbId = user.uid
                                        parentFbName = user.name

                                         #store the parentFb id
                                        await client.send(Message(text="Dear "+str(parentFbName)+", Your child : "+str(myFirstCard)+" checked out at "+str(todaytime)+ ", in the date of, "+str(today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                        refresh("---","message sended ","to fb checkout ","----")

                                    time.sleep(3)
                                else:
                         
                         ###############if the card does not in the list
                                    print("card invalid")
                                    refresh("---","card invalid","card invalid","----")

                            elif studentCardStatus == "Invalid".casefold():
                                print("student card invalid")
                                refresh("---","student card invalid","card invalid","----")

                            elif studentCardStatus == "None".casefold():
                                print("cannot use parent card")
                                refresh("------------","Card not registed yet","please use registered card","--------")
                            else:
                                refresh("------------","Card not useable","please use registered card","--------")

                                
                        except:
                            print("£££Something when wrong£££")
                        
                      
                     #print(str(myFirstCardId),"printed in string")
                        #check for duplicated entry
                       

            
    finally:
            GPIO.cleanup()


client.loop.run_until_complete(main())





