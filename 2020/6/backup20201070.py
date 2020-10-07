
import board
import busio as io
import adafruit_mlx90614

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
from pyzbar.pyzbar import decode
from PIL import Image
from urllib import request, parse
from urllib.request import Request, urlopen
from datetime import datetime
from datetime import date
import smtplib, ssl
import subprocess
import time

import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from threading import Event
from picamera.array import PiRGBArray
from picamera import PiCamera
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

def connectSql():
    try:
        conn = mysql.connector.connect(
            
            host="194.59.164.64",
            user="u615769276_wcid",
            passwd="Password123",
            database="u615769276_wcid"
        )
        return conn
    except Exception as e:
        print(e)
        
global conn
conn = connectSql()
print(conn)

def validStaff(qrid, qrname,conn):
    # check wherther the card punch card today or not if return any row then yes
    query = """SELECT * FROM staff WHERE staffID = '%s' AND staffName = '%s'""" % (
        (qrid), qrname)
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
           # returnResult = ''
           # for x in final_result:
             #   returnResult = ''.join(i for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return len(result)
        else:
            return 0
    except Error as error:
        print(error)

    finally:
        cursor.close()

def getCheckOut(staffId,conn):
    query = """SELECT checkOut FROM stafflog WHERE staffId = '%s' AND checkOut IS NOT NULL ORDER BY staffLogId DESC""" % (
        (staffId))
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
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(str(i) for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return 0
    except Error as error:
        print(error)

    finally:
        cursor.close()

def getStatus(staffId,conn):
    query = """SELECT checkIn FROM stafflog WHERE staffId = '%s' AND checkIn IS NOT NULL ORDER BY staffLogId DESC LIMIT 1""" % (
        (staffId))
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
        if len(result) > 0:
            # if more than one row result

            bad_chars = [';', ':', '!', "*", "'", "[", "]", "(", ")", ",", "'"]
            # remove all invalid character
            returnResult = ''
            for x in final_result:
                returnResult = ''.join(str(i) for i in x if not i in bad_chars)
                # loop thought the result and get only one result
            return returnResult
        else:
            return 0
    except Error as error:
        print(error)

    finally:
        cursor.close()
#print(getStatus(7,conn))      
def insertStaffLog(staffId,staffName,temperature,status,conn,todayTime,today):
    cursor = conn.cursor(buffered=True)
    try:

        sql_insert_query = """INSERT INTO stafflog (staffId,staffName,checkIn,temperature,time,date) VALUES (%s,%s,%s,%s,%s,%s)"""
        
        insert_tuple = (
            staffId,staffName,status,temperature,todayTime,today)
        cursor.execute(sql_insert_query, insert_tuple)
        conn.commit()

        return "Insert StaffLog Success"

    except mysql.connector.Error as error:
        return "error table parameterized query failed {}".format(error)

    finally:
        cursor.close()
        
def detectmaskfirst():
    model = load_model('models/mask_detector.h5')
    #cap = cv2.VideoCapture(0)

    #camera = PiCamera()
   # camera.rotation = 180
    # camera.framerate = 32
    #rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


    #detector = cv2.QRCodeDetector()
    def detect_mask(image):
        copy_img = image.copy()
        print(copy_img)
        resized = cv2.resize(copy_img, (254, 254))

        resized = img_to_array(resized)
        resized = preprocess_input(resized)

        resized = np.expand_dims(resized, axis=0)
        
        mask, _ = model.predict([resized])[0]

        return mask


    #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        #img = frame.array
    ret = True

    while ret:

     #   cap = cv2.VideoCapture(0)
       # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        
        _, img = cap.read()
        mask_prob = detect_mask(img)
        print(mask_prob)
        if mask_prob > 0.5:
            cv2.putText(img, 'Mask Detected', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 0), 3)
            
            print("mask detected")
            cap.release()
            cv2.destroyAllWindows()
            #break
            return "mask found"

           # cap.release()
           # return "mask found"
           # break
        
        elif mask_prob < 0.5:
             print("no mask")
             cv2.putText(img, 'No Mask', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
 
#             for i in range(5):
#                 time.sleep(2)
#                 cv2.putText(img, 'No Mask' + str(i), (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
#                 cv2.imshow('window', img)
#             print("no mark detected")
              
        cv2.imshow('window', img)

    # else:
     #   cv2.imshow('window', img)
    
       # rawCapture.truncate(0)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
        elif key == ord('a'):
            cv2.imwrite('my_pic.jpg', img)


    cv2.destroyAllWindows()

def runcamera(temperature):
    #cap.release()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    conn = connectSql()
    detector = cv2.QRCodeDetector()

    print("Place Qr code infront of the camera to scan...")
    while (cap.isOpened()):

        _, img = cap.read()
        
        data, bbox, _ = detector.detectAndDecode(img)

        if (bbox is not None):
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255,
                                                                                             0, 255), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

            if data:
                #buzzer.buzzerOn()
                print("data found: ", data)
                #conn = connectSql()

                try:

                    qrcodeArr = data.split(",")
                    todayTime  = datetime.now().time().replace(microsecond=0)
                    print(todayTime)
                    today = date.today()
                    print(today)
                 #   TimeNow = (datetime.now().strftime("%H:%M"))
                  #  todayTime  = datetime.now().time().replace(microsecond=0)
                    print("Reading qr code.....")
                    #c#heckBooking(qrcodeArr[0], qrcodeArr[1], qrcodeArr[2], qrcodeArr[3], todayTime,conn)
                   # sys.exit()
                    print(qrcodeArr)
                    staffValid = validStaff(qrcodeArr[0],qrcodeArr[1],conn)
                    print(staffValid)
                    if(int(staffValid) >= 1):
                        #if staff ada
                        checkInStatus = getStatus(qrcodeArr[0],conn)
                        
                        print(checkInStatus)
                        if(checkInStatus == "checkIn"):
                            result = insertStaffLog(qrcodeArr[0],qrcodeArr[1],temperature,"checkOut",conn,todayTime,today)
                            #if user already check in then check out him
                             
                        else:
                            result = insertStaffLog(qrcodeArr[0],qrcodeArr[1],temperature,"checkIn",conn,todayTime,today)
                          #  checkOutStatus = getCheckOut(7,conn)
                            #if user havent checkout last record
                          #  print(checkOutStatus)
                        print(result)
                        qrcode = "valid"
                    else:
                        qrcode = "invalid"
                    #qrcode = "invalid"
                    
                    root = Tk()
                   
                    root.title("Qr code status")
                    lbl1 = Label()
                    lbl1.config(height=50,width=50, font=('times', 20, 'bold'))
                    lbl1.pack(fill=BOTH, expand=1)
                    lbl1.config(fg='white')
                    
                    if(qrcode == "valid"):
                        
                        print("qr code valid")
                        lbl1.config(bg='green')
        
                        #lbl1["text"] = "Your temperature is " + str(temp)
                        lbl1["text"] = "Your qr code is valid" 
                       # root.after(2222,root.destroy())
                        for k in range(4, 0, -1):
                            lbl1["text"] = "Your qr code is valid"
                            root.update()
                            time.sleep(1)
                            print(k)
                            if(k == 1):
                                lbl1.destroy()
                            #display temp for 5 sec
                        root.destroy()
                        #root.destroy()
                        time.sleep(2)
                        cap.release()
                       # cv2.destroyAllWindows()
                        cap = cv2.VideoCapture(0)
                        print("qrcode valid")
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                        break
                    if(qrcode == "invalid"):
                        
                        print("qr code not valid")
                        lbl1.config(bg='red')
        
                        #lbl1["text"] = "Your temperature is " + str(temp)
                        lbl1["text"] = "Your qr code is invalid" 
                       # root.after(2222,root.destroy())
                        for k in range(4, 0, -1):
                            lbl1["text"] = "Your qr code is invalid"
                            root.update()
                            time.sleep(1)
                            print(k)
                            if(k == 1):
                                lbl1.destroy()
                            #display temp for 5 sec
                        root.destroy()
                        #root.destroy()
                        time.sleep(2)
                        cap.release()
                       # cv2.destroyAllWindows()
                        cap = cv2.VideoCapture(0)
                        print("qrcode valid")
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                        break
                except Exception as e:
                    print(e)

                    print("Invalid Qr code.....")

                    #      cap.release()
                    #     cv2.destroyAllWindows()


                    tkinter.messagebox.showwarning(title="Error",
                                                   message="Invalid Qr Code\nPlease use valid qr code for booking")
                    #sys.exit()

        cv2.imshow("code detector", img)
        if (cv2.waitKey(1) == ord("q")):
            break
    cap.release()
    cv2.destroyAllWindows()
def scanTemp():
    print("scan temp after 5 sec")
    root = Tk()
    root.title("Scan temperature ...")
    lbl1 = Label()
    lbl1.pack(fill=BOTH, expand=1)
    countDown(lbl1,root)
    
    #root.destroy()
    i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90614.MLX90614(i2c)

    # temperature results in celsius
    print("Ambent Temp: ", mlx.ambient_temperature)
    print("Object Temp: ", mlx.object_temperature)
    return mlx.object_temperature

def countDown(lbl1,root):
    lbl1.config(bg='yellow')
    lbl1.config(height=50,width=50, font=('times', 20, 'bold'))
   # lbl1.place(relx=0.5, rely=0.5, anchor=CENTER)

    for k in range(4, 0, -1):
        lbl1["text"] ="Scan your temperature after " +str(k) + " sec" 
        root.update()
        time.sleep(1)
    lbl1.config(bg='red')
    lbl1.config(fg='white')
    lbl1["text"] = "Please scan your temperature now!"
    root.destroy()
def displayTemp(temp):
    root = Tk()
    if(temp < 37.5):
        
        root.title("Can enter")
    else:
        root.title("Cannot enter")
    lbl1 = Label()
    lbl1.config(height=50,width=50, font=('times', 20, 'bold'))
    lbl1.pack(fill=BOTH, expand=1)
    lbl1.config(fg='white')
    
    if(temp < 37.5 and temp >32):
        lbl1.config(bg='green')
        
        lbl1["text"] = "Your temperature is " + str(temp)
       # root.after(2222,root.destroy())
        for k in range(4, 0, -1):
            lbl1["text"] = "Your temperature is " + str(temp) 
            root.update()
            time.sleep(1)
            print(k)
            if(k == 1):
                lbl1.destroy()
            #display temp for 5 sec
        root.destroy()
        #root.destroy()
        time.sleep(2)
        
        #root.destroy()
        #time.sleep(2)
        #()
    else:
        #if temp bigger than normal
        lbl1.config(bg='red')
        
        #lbl1["text"] = "Your temperature is " + str(temp)
        lbl1["text"] = "Your temperature is " + str(temp)
       # root.after(2222,root.destroy())
        for k in range(4, 0, -1):
            lbl1["text"] = "Your temperature is " + str(temp) 
            root.update()
            time.sleep(1)
            print(k)
            if(k == 1):
                lbl1.destroy()
            #display temp for 5 sec
        root.destroy()
        #root.destroy()
        time.sleep(2)
        
    
 
def welcome(temp):
     MSG = '''Thank you.

     Your temperature is '''+str(temp)+'''.
     .'''
     top = Toplevel()
     if(int(temp) < 37.5):
         
         Message(top, text=MSG + "\nYou are allow to enter", padx=30, pady=30).pack()
         top.after(8000, top.destroy)
         
     else:
         top.title('Sorry')
         Message(top, text=MSG + "\nYou are NOT allow to enter", padx=30, pady=30).pack()
         top.after(8000, top.destroy)

#detectmaskfirst()
#detectmaskfirst()
##temp = scanTemp()
#welcome(temp)
#Event().wait(3.0)

while True:
    if(detectmaskfirst() == "mask found"):
        temp = scanTemp()
        displayTemp(temp)
        if(temp < 37.5 and temp >32):

            runcamera(temp)
            #insert temp
 

                        


##displayTemp(temp)

#t=5
#while t: 
#    mins, secs = divmod(t, 60) 
#    timer = '{:02d}:{:02d}'.format(mins, secs) 
#    print(timer, end="\r") 
#    time.sleep(1) 
#    t -= 1
# time.sleep(3)
#runcamera()


