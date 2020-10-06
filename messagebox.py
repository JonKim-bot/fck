
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

from picamera.array import PiRGBArray
from picamera import PiCamera

def detectmaskfirst():
    model = load_model('models/mask_detector.h5')
    cap = cv2.VideoCapture(0)

    camera = PiCamera()
    camera.rotation = 180
    # camera.framerate = 32
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)


    def detect_mask(image):
        copy_img = image.copy()

        resized = cv2.resize(copy_img, (254, 254))

        resized = img_to_array(resized)
        resized = preprocess_input(resized)

        resized = np.expand_dims(resized, axis=0)

        mask, _ = model.predict([resized])[0]

        return mask


    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        ret = True

        if ret:

            mask_prob = detect_mask(img)

            if mask_prob > 0.5:
                cv2.putText(img, 'Mask Detected', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 0), 3)

                print("mask detected")
                cv2.destroyAllWindows()



                cap.release()
                return "mask found"
                break
            
            elif mask_prob < 0.5:
                 cv2.putText(img, 'No Mask', (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
     
    #             for i in range(5):
    #                 time.sleep(2)
    #                 cv2.putText(img, 'No Mask' + str(i), (200, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)
    #                 cv2.imshow('window', img)
    #             print("no mark detected")
                  
            cv2.imshow('window', img)

        else:
            cv2.imshow('window', img)
        
        rawCapture.truncate(0)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
        elif key == ord('a'):
            cv2.imwrite('my_pic.jpg', img)


    cv2.destroyAllWindows()

def runcamera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


    detector = cv2.QRCodeDetector()

    print("Place Qr code infront of the camera to scan...")
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
                #buzzer.buzzerOn()
                print("data found: ", data)
                #conn = connectSql()

                try:

                    qrcodeArr = data.split(",")
                    
                    TimeNow = (datetime.now().strftime("%H:%M"))
                    todayTime  = datetime.now().time().replace(microsecond=0)
                    print("Reading qr code.....")
                    #c#heckBooking(qrcodeArr[0], qrcodeArr[1], qrcodeArr[2], qrcodeArr[3], todayTime,conn)
                    sys.exit()

                except Exception as e:
                    print(e)

                    print("Invalid Qr code.....")

                    #      cap.release()
                    #     cv2.destroyAllWindows()


                    tkinter.messagebox.showwarning(title="Error",
                                                   message="Invalid Qr Code\nPlease use valid qr code for booking")
                    sys.exit()

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

    for k in range(2, 0, -1):
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
    
    if(temp < 37.5):
        lbl1.config(bg='green')
        
        lbl1["text"] = "Your temperature is " + str(temp)
        root.after(2222, root.destroy)
        #root.destroy()
        #time.sleep(2)
        #()
    else:
        lbl1.config(bg='red')
        
        lbl1["text"] = "Your temperature is " + str(temp)
        
    
 
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

#if(detectmaskfirst() == "mask found"):
temp = scanTemp()
welcome(temp)
#displayTemp(temp)
t=5
while t: 
    mins, secs = divmod(t, 60) 
    timer = '{:02d}:{:02d}'.format(mins, secs) 
    print(timer, end="\r") 
    time.sleep(1) 
    t -= 1
# time.sleep(3)
#runcamera()

