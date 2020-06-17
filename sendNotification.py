from urllib import request, parse
from urllib.request import Request, urlopen

import urllib.parse
import urllib.request
#import requests


#url = "https://piegensoftware.com/NotificationSystemInPHP-master/testingNotification/notification.php"
#url = "https://piegensoftware.com/NotificationSystemInPHP-master/testingNotification/sendbyuserid.php"

#url = 'https://www.zomato.com/praha/caf%C3%A9-a-restaurant-z%C3%A1ti%C5%A1%C3%AD-kunratice-praha-4/daily-menu'
#u#rl = "http://boitanpow.000webhostapp.com/myhtp.php"

#url = "https://piegensoftware.com/NotificationSystemInPHP-master/insertMsg.php"
#url = "http://boitanpow.000webhostapp.com/NotificationSystemInPHP-master/insertMsg.php"
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

sendNotifications(867364651663,"Hola caojibai boitiiiannta")