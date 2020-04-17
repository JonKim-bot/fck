import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import time
from difflib import SequenceMatcher
import urllib.parse
import urllib.request
import json
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


mydb = mysql.connector.connect(
  host="localhost",
  user="mydb",
  passwd="password",
  database="hydro"

)
mycursor = mydb.cursor()


def insertParent(firstCard,FCName):
    try:
        url = 'http://boitanpow.000webhostapp.com/myhtp.php'
        values = {'firstcard': firstCard,
                  'fcname': FCName,
                  'insertFCard': '' }

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
           the_page = response.read()
        print(the_page.decode())
    except Exception as e:
        print(e)

def insertStudent(Secard,SCName):
    try:
        url = 'http://boitanpow.000webhostapp.com/myhtp.php'
        values = {'Secard': Secard,
                  'Scname': SCName,
                  'insertStudentCard': '' }

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
           the_page = response.read()
        print(the_page.decode())
    except Exception as e:
        print(e)
        
def updateStudent(Secard,SCName,firstCard):
    try:
        url = 'http://boitanpow.000webhostapp.com/myhtp.php'
        values = {'Secard': Secard,
                  'Scname': SCName,
                  'firstCard' : firstCard,
                  'updateStudent': '' }

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
           the_page = response.read()
        print(the_page.decode())
    except Exception as e:
        print(e)

def updateParent(firstCard,FCName,Secard):
    try:
        url = 'http://boitanpow.000webhostapp.com/myhtp.php'
        values = {'firstCard': firstCard,
                  'FCName': FCName,
                  'Secard' : Secard,
                  'updateParent': '' }

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
           the_page = response.read()
        print(the_page.decode())
    except Exception as e:
        print(e)


def returnParentIds():
     parentList = []
     try:
            url = 'http://boitanpow.000webhostapp.com/myhtp.php'
            values = {
                     
                      'returnParents': '' }

            data = urllib.parse.urlencode(values)
            data = data.encode('ascii')
            req = urllib.request.Request(url, data)
            with urllib.request.urlopen(req) as response:
               the_page = response.read()
            parentList = the_page.decode().split(",")
            return str(parentList)
     except Exception as e:
            print(e)#
def returnStudentIds():
     StudentList = []
     try:
            url = 'http://boitanpow.000webhostapp.com/myhtp.php'
            values = {
                     
                      'returnStudents': '' }

            data = urllib.parse.urlencode(values)
            data = data.encode('ascii')
            req = urllib.request.Request(url, data)
            with urllib.request.urlopen(req) as response:
               the_page = response.read()
            StudentList = the_page.decode().split(",")
            return str(StudentList)
            #return a list of list
                
     except Exception as e:
            print(e)#
print(returnStudentIds(),"is ids")

#print(returnParentIds())
reader = SimpleMFRC522()

try:
        while True:
                    studentCardList = [943343799769]
                    parentCardList = [867364651663]
                    #store the list of card to check
                    counter = 0
                    print("Scan your first card")
                    id1, text = reader.read()
                    #get the id and name of the card
                    #print(id)
                    #print(text)
                    counter = counter + 1
                    #print("Num of time :",counter)
                    # print how many time it scan
                    
                    #do a validation that cannot scan the card twice
                    #can be done by forcing all the 4 column to be the diffrent value or comparison with the value that previosly inserted
                    
                    myFirstCard = text
                    myFirstCardId = id1
                    
                    #print(str(myFirstCardId),"printed in string")
                    #check for duplicated entry
                    if str(myFirstCardId) in returnStudentIds():
                        print("duplicated entry")
                    else:
                        #if not duplicated entry then
                        print("valid entry")
                        #first time is insert 
                        if myFirstCardId in parentCardList:
                            insertParent(myFirstCardId,myFirstCard)
                            print("Inserted to parent Card")
                        elif myFirstCardId in studentCardList:
                            insertStudent(myFirstCardId,myFirstCard)
                            print("Inserted to student card")
                        else:
                            print("FirstCard Is not in the list")
                    time.sleep(5)
                    print("Scan your Second card")
                    #READ THE SECCARD data
                    id, text2 = reader.read()
                    mySecCard = text2
                    mySecCardId = id
                    #if the first card is scanned twice then print 
                    if mySecCardId != myFirstCardId:
                        if str(mySecCardId) in returnParentIds() or str(mySecCardId) in returnStudentIds():
                            print("duplicated entry")
                        else:
                            print("valid entry")
                            if mySecCardId in parentCardList:
            
                                updateParent(mySecCardId,mySecCard,myFirstCardId)
                                print("Updated to parent Card")
                            elif mySecCardId in studentCardList:
                                updateStudent(mySecCardId,mySecCard,myFirstCardId)
                                print("Updated to student card")
                            else:
                                print("Second Card Is not in the list")
                    else:
                        print("Duplicated Scaning")
                    print("First Card Name : ",myFirstCard)
                    
                    print("Second Card Name: ",mySecCard)
                    time.sleep(3)
                    
                    #insertFCard(myFirstCardId,myFirstCard,mySecCardId,mySecCard)
                    #insert the record in to database 4 column
                    #print(type(myFirstCard))
                    
                    if similar(str(myFirstCard),"KimberyFather") > 0.7 and similar(str(mySecCard),"KimberySan") > 0.7:
                        print("Authenticated")
                    else:
                        print("Not authenticated")

        
finally:
        GPIO.cleanup()




