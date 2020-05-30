import cv2
import os
import tkinter
from tkinter import *
from PIL import Image
#import RPi.GPIO as GPIO

from PIL import ImageTk
from mysql.connector import Error
import mysql.connector
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306

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

def connectSql():
    conn = mysql.connector.connect(
        host="194.59.164.64",
        user="u615769276_boitan",
        passwd="password",
        database="u615769276_finalyear"
    )
    return conn


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

                   # refresh("-----------------", "qr code able", "to use", "--------------------")
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
                    #ledLightOnGreen()

                elif finalData == "Not Valid":
                    #refresh("-----------------", "qr code expired ", "not able to use", "--------------------")

                    #ledLightOnRed()
                    print("qr code expired")
                    tkinter.messagebox.showinfo(title="Qr Code Not Valid", message="qr code expired")

                elif finalData == "No Record Found":
                    #refresh("-----------------", "No booking found ", "qr code expired", "--------------------")
                   # ledLightOnRed()

                    tkinter.messagebox.showwarning(title="No Booking Record Found",
                                                  message="No Booking Record Found , Please make the booking first.")

                    print("No Booking Record Found , Please make the booking first.")
            else:
                tkinter.messagebox.showwarning(title="Time Not Reached Yet",
                                               message="Time Now Are Not With in the range")
             #   ledLightOnRed()

                print("Booking Time Not With In The Range")
        else:
            tkinter.messagebox.showwarning(title="Booking Date are not today",
                                           message="Booking Date are not today,please try again with another qr code")

            print("Booking Date are not today!")
            #ledLightOnRed()

    except Error as error:
        print(error)

        # get the currrent time in hour and minit format


def isNowInTimePeriod(startTime, endTime, nowTime):
    # check if the time are with in the range , if not then cannot use qrcode
    if startTime < nowTime and nowTime < endTime:
        return True
    else:
        return False

cap = cv2.VideoCapture(0)

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
                qrcodeArr = data.split(",")
                print(qrcodeArr[0])
                print(qrcodeArr[1])
                print(qrcodeArr[2])
                print(qrcodeArr[3])
                TimeNow = (datetime.now().strftime("%H:%M"))
                todayTime = datetime.now().time()
                print(todayTime)
                checkBooking(qrcodeArr[0], qrcodeArr[1], qrcodeArr[2], qrcodeArr[3], todayTime)
            except Exception as e:
                print(e)
                tkinter.messagebox.showwarning(title="Error",
                                               message="Invalid Qr Code\nPlease use qr code for booking")
    cv2.imshow("code detector", img)
    if (cv2.waitKey(1) == ord("q")):
        break
cap.release()
cv2.destroyAllWindows()