import os
import tkinter
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import tkinter.messagebox
import cv2
import pyqrcode
from pyzbar.pyzbar import  decode
from PIL import Image
from urllib import request, parse
from urllib.request import Request, urlopen

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import smtplib, ssl

from datetime import datetime
from datetime import date


from urllib.error import HTTPError
import  time
count = 0
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
def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 5 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
def select_image():
        # grab a reference to the image panels
        global panelA
        global count
        global qrDataDisplayName
        global qrDataDisplayDate
        global qrDataDisplayTimeOne
        global qrDataDisplayTimeTwo
        global fileName
        global buttonVerify




        # open a file chooser dialog and allow the user to select an input
        # image
        path = filedialog.askopenfilename()
        try:
            def sendEmail(email):
                port = 587  # For starttls
                smtp_server = "smtp.gmail.com"
                sender_email = "chinli2001123@gmail.com"
                receiver_email = email
                password = ("walaodiam123")
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
                try:#check if student check in already or not lah
                    
                    url = 'https://piegensoftware.com/myhtp.php'
                    values = {'getEmail': '',
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
            def getParentId(studentName,pickUpDate,pickUpTimeOne,pickUpTimeTwo):
                url = 'https://piegensoftware.com/myhtp.php'
                values = {
                         'getIdQr':"1",
                        # 'updateBooking': "1",
                        'studentName': studentName,
                        'pickUpDate': pickUpDate,
                        'pickUpTimeOne': pickUpTimeOne,
                        'pickUpTimeTwo': pickUpTimeTwo,                       
                          }

                data = parse.urlencode(values).encode()
                req = Request(url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                    ,data=data)
                webpage = urlopen(req).read().decode()
                return (webpage)
            
            def checkBooking(studentName,pickUpDate,pickUpTimeOne,pickUpTimeTwo,todayTime):




            #check booking data by passing all data inhere
                try:
                    url = "https://piegensoftware.com/myhtp.php"
                    data = {
                        'checkBooking':"1",
                        # 'updateBooking': "1",
                        'timeNow' : todayTime,

                        'studentName': studentName,
                        'pickUpDate': pickUpDate,
                        'pickUpTimeOne': pickUpTimeOne,
                        'pickUpTimeTwo': pickUpTimeTwo,
                    }

                    data = parse.urlencode(data).encode()
                    TimeNow = (datetime.now().strftime("%H:%M"))
                    today = date.today()
                    print(today)
                    if(str(today) == str(pickUpDate)):
                        #if date are not today , stop running the system
                    #get the currrent time in hour and minit format
                        if (isNowInTimePeriod(pickUpTimeOne,pickUpTimeTwo,TimeNow)) == True:
                            #if time are with in the range then request

                            req = Request(
                                    url,
                                    headers={'User-Agent': 'Mozilla/5.0'}
                                    ,data=data)
                            webpage = urlopen(req).read().decode()
                            print(webpage)
                            if webpage == "Valid":
                                refresh("-----------------","qr code able","to use","--------------------")
                                parentId = getParentId(studentName,pickUpDate,pickUpTimeOne,pickUpTimeTwo)
                                #get parent id from tblparentbooking
                                print(parentId)
                                parentEmail = getEmail(parentId)
                                #get email by passing the parent id
                                print("parent email",parentEmail)
                                sendEmail(parentEmail)
                                #send confirm email
                                print("can bring children home")
                                tkinter.messagebox.showinfo(title="Valid Qr Code", message="can bring children home")
                                ledLightOnGreen()
                                
                            elif webpage == "Not Valid":
                                refresh("-----------------","qr code expired ","not able to use","--------------------")

                                print("qr code expired")
                                
                                tkinter.messagebox.showinfo(title="Qr Code Not Valid", message="qr code expired")

                            elif webpage == "No Record Found":
                                refresh("-----------------","No booking found ","qr code expired","--------------------")

                                tkinter.messagebox.showwarning(title="No Booking Record Found", message="No Booking Record Found , Please make the booking first.")


                                print("No Booking Record Found , Please make the booking first.")
                        else:
                            tkinter.messagebox.showwarning(title="Time Not Reached Yet",
                                                           message="Time Now Are Not With in the range")

                            print( "Booking Time Not With In The Range")
                    else:
                        tkinter.messagebox.showwarning(title="Booking Date are not today",
                                                           message="Booking Date are not today,please try again with another qr code")

                        print( "Booking Date are not today!")

                        

                except HTTPError as e:

                     content = e.read()
                     print(e)
            #return the response

            def clearWidget():
                #clear widget on the form after it reload to prevent duplication
                list = root.pack_slaves()
                for l in list:

                    fileName.destroy()
                    
                    qrDataDisplayName.destroy()
                    qrDataDisplayDate.destroy()
                    qrDataDisplayTimeTwo.destroy()
                    qrDataDisplayTimeOne.destroy()

                    buttonVerify.destroy()

            def isNowInTimePeriod(startTime, endTime, nowTime):
                #check if the time are with in the range , if not then cannot use qrcode
                if startTime < nowTime and nowTime < endTime:
                     return True
                else:
                     return False
            if len(path) > 0:
                # load the image from disk, convert it to grayscale, and detect
                # edges in it
                image = cv2.imread(path)
                oriname = os.path.basename(path)
                if "qrcode" in path:
                    qrcodeData = decode(Image.open(oriname))
                    print("In qrcode file - -- ")
                else:
                    qrcodeData = decode(Image.open(path))
                    print("not in qrcode file")
                print(oriname)
                print(path)
                qrcode = (qrcodeData[0].data.decode('utf8'))
                qrcodeArr = qrcode.split(",")
                print(qrcodeArr[0])
                print(qrcodeArr[1])
                print(qrcodeArr[2])
                print(qrcodeArr[3])

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # OpenCV represents images in BGR order; however PIL represents
                # images in RGB order, so we need to swap the channels
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # convert the images to PIL format...
                image = Image.fromarray(image)
                # ...and then to ImageTk format
                image = ImageTk.PhotoImage(image)
                if panelA is None and count < 1:

                    # the first panel will store our original image
                    panelA = Label(image=image)
                    panelA.image = image
                    panelA.pack(side="left", padx=10, pady=10)
                    TimeNow = (datetime.now().strftime("%H:%M"))
                    todayTime = datetime.now()
                    print(todayTime)
                    
                    fileName = Label(root, text="Date Today : "+datetime.now().strftime("%m-%d-%Y")+"\n\nTime Now : "+TimeNow+"\n\nQR Code Info:\n\nFile Name = "+str(oriname),font=("Helvetica", 16))
                    fileName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayName = Label(root, text="QR CODE NAME = " + str(qrcodeArr[0]),bg="black",fg="white",font=("Helvetica", 16))
                    qrDataDisplayDate = Label(root, text="QR CODE DATE = " + str(qrcodeArr[1]),font=("Helvetica", 16))
                    qrDataDisplayTimeOne = Label(root, text="QR CODE TIME START FROM = " + str(qrcodeArr[2]),bg="black",fg="white",font=("Helvetica", 16))
                    qrDataDisplayTimeTwo = Label(root, text="QR CODE = TIME END = " + str(qrcodeArr[3]),font=("Helvetica", 16))

                    qrDataDisplayName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayDate.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayTimeOne.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayTimeTwo.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    buttonVerify = tkinter.Button(text='Verify', width=25,command= lambda: checkBooking(qrcodeArr[0],qrcodeArr[1],qrcodeArr[2],qrcodeArr[3],todayTime),font=("Helvetica", 16))
                    buttonVerify.pack()
                    #pass this lambda function to get thogught
                    count = count + 1
                    print(count)

                    print("open image ")
                    # while the second panel will store the edge map

                    # otherwise, update the image panels
                elif(count >= 1):
                    clearWidget()
                    count = count + 1
                    print(count)

                    # update the pannels
                    panelA.configure(image=image)
                    panelA.image = image
                    TimeNow = (datetime.now().strftime("%H:%M"))
                    todayTime = datetime.now()
                    print(todayTime)
                    fileName = Label(root, text="Date Today : " + datetime.now().strftime(
                        "%m-%d-%Y") + "\n\nTime Now : " + TimeNow + "\n\nQR Code Info:\n\nFile Name = " + str(oriname),
                                     font=("Helvetica", 16))
                    fileName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayName = Label(root, text="QR CODE NAME = " + str(qrcodeArr[0]),bg="black",fg="white",font=("Helvetica", 16))
                    qrDataDisplayDate = Label(root, text="QR CODE DATE = " + str(qrcodeArr[1]),font=("Helvetica", 16))
                    qrDataDisplayTimeOne = Label(root, text="QR CODE TIME START FROM = " + str(qrcodeArr[2]),bg="black",fg="white",font=("Helvetica", 16))
                    qrDataDisplayTimeTwo = Label(root, text="QR CODE = TIME END = " + str(qrcodeArr[3]),font=("Helvetica", 16))

                    qrDataDisplayName.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayDate.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayTimeOne.pack(side=TOP, anchor=W, fill=X, expand=YES)
                    qrDataDisplayTimeTwo.pack(side=TOP, anchor=W, fill=X, expand=YES)

                    buttonVerify = tkinter.Button(text='Verify', width=25,command= lambda: checkBooking(qrcodeArr[0],qrcodeArr[1],qrcodeArr[2],qrcodeArr[3],todayTime),font=("Helvetica", 16))
                    buttonVerify.pack()

                    print("open image 2")

        except Exception  as e:
             print(e)

             tkinter.messagebox.showerror(title=None, message="Not A Valid Qr Code")


# initialize the window toolkit along with the two image panels
root = Tk()

root.title("Qr Code Information")
center(root)
app=FullScreenApp(root)

panelA = None
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Click Me to Select an qr code", command=select_image,font=("Helvetica", 16))
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
# kick off the GUI
root.mainloop()

#first step , scan and display the data ,

#compare the data by using , select * from booking table where qrcode is not scanned
#if got record then green light
#after green light , update the record to make it scanned


