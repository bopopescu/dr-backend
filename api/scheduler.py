import schedule
import time
import requests, json
import urllib
import urllib2
import datetime

def sendSMSLocal(apikey, numbers, sender, message):
    data =  urllib.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib2.Request("https://api.textlocal.in/send/?")
    f = urllib2.urlopen(request, data)
    fr = f.read()
    return(fr)

def getToken():
    API_ENDPOINT = "http://localhost:8080/login/"
    data = {'email':"karan@drtangri.com",
            'password':'batman25'}
    r = requests.post(url = API_ENDPOINT, data = data)
    res = r.json()
    print res
    access_token=res['access_token']
    return str(access_token)

def getAppointmentsMessages():
    print "..start scheduler.."
    print datetime.datetime.now()
    API_ENDPOINT = "http://localhost:8080/api/appointmentmessage/"
    token = getToken()
    auth="Bearer "+token
    r = requests.get(url = API_ENDPOINT, headers={"Authorization":auth})
    res = r.json()
    print "bhai.."
    print res

# schedule.every(0.05).minutes.do(job)
# schedule.every().hour.do(job)
schedule.every().day.at("8:00").do(getAppointmentsMessages)
# schedule.every().day.at("12:56").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
