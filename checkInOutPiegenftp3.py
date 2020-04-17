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
client = Client()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


mydb = mysql.connector.connect(
  host="localhost",
  user="mydb",
  passwd="password",
  database="hydro"

)
mycursor = mydb.cursor()

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
#print(allStudrecord(),"is student record")
newStudentList = []


#print(CheckIfNotNull('943343799769','2019-12-19'),"is check if not null")
async def main():
    await client.start("0169787592", "woqunima123")    
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
                        print("Scan your Card to record attendance")
                        id1, text = reader.read()
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
                        
                        #print(myCardId,"is card")
                        try:
                            if checkCardCheckin(myCardId,today) == str(1) :
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
                                    parentId = findParentId(myCardId)
                                    #print(parentId ,"is parent id")
                                    #get the parent id for search it in the email or fb
                                    user =(await client.search_for_users(findFbId(parentId)))[0]
                                    parentFbId = user.uid
                                    parentFbName = user.name

                                    #store the parentFb id
                                    await client.send(Message(text="Dear "+str(parentFbName)+"Your child : "+str(myFirstCard)+" checked in at "+str(todaytime) + ", in the date of, "+str(today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                    time.sleep(3)
                                    #if the student already check in then update the check up
                                else:
                                    #
                                    print("updating the checwwwwwk out")
                                    updateCheckOut(myCardId,todaytime)
                                    parentId = findParentId(myCardId)
                                    #get the parent id for search it in the email or fb
                                    user =(await client.search_for_users(findFbId(parentId)))[0]
                                    parentFbId = user.uid
                                    parentFbName = user.name

                                 #store the parentFb id
                                    await client.send(Message(text="Dear "+str(parentFbName)+", Your child : "+str(myFirstCard)+" checked in at "+str(todaytime)+ ", in the date of"+str(today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                    time.sleep(3)
                                    
                            elif checkAttendance(myCardId,today) == "present":
                                #add one more condition to check whether if he or she is present today
                                print("punch card already today can go back ")
                                time.sleep(3)
                            
                            elif int(checkCard(myCardId,today)) >=1 and CheckIfNotNull(myCardId,today) != "None":
                                #if the check in is not null and already insert today but the card 
                                #print("punch check in already")
                                print("updating the check out")
                                updateCheckOut(myCardId,todaytime)
                                insertCheckoutNotification(myCardId,todaytime,today)

                                parentId = findParentId(myCardId)
                                    #get the parent id for search it in the email or fb
                                user =(await client.search_for_users(findFbId(parentId)))[0]
                                parentFbId = user.uid
                                parentFbName = user.name

                                 #store the parentFb id
                                await client.send(Message(text="Dear "+str(parentFbName)+", Your child : "+str(myFirstCard)+" checked out at "+str(todaytime)+ ", in the date of, "+str(today)), thread_id=int(parentFbId), thread_type=ThreadType.USER)
                                time.sleep(3)
                            else:
                                ###############if the card does not in the list
                                print("card invalid")
                        except:
                            print("£££Something when wrong£££")
                        
                      
                     #print(str(myFirstCardId),"printed in string")
                        #check for duplicated entry
                       

            
    finally:
            GPIO.cleanup()


client.loop.run_until_complete(main())



