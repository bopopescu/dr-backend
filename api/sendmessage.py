# import urllib2
# import urllib
import requests, json
import urllib
import urllib2

def sendSMS(number, text):
    r = requests.get(url = 'http://198.24.149.4/API/pushsms.aspx?loginID=drtangri&password=abc123&mobile='+str(number)+'&text='+text+'&senderid=DEMOOO&route_id=7&Unicode=0')
    pastebin_url = r.text
    return pastebin_url


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
    data = {'email':"tangri@gmail.com",
            'password':'batman25'}
    r = requests.post(url = API_ENDPOINT, data = data)
    res = r.json()
    access_token=res['access_token']
    return str(access_token)
