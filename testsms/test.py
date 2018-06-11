import urllib.request
import urllib.parse

def sendSMS(username, password,  numbers, sender, message):
    data =  urllib.parse.urlencode({'username':username, 'password':password,  'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

resp =  sendSMS('drkarantangri@gmail.com','Karan_12345', '9953809852',
    'Jims Autos', 'Mr/Ms. Deepak, Your appointment has been booked for 10-10-2018 at 7:00 PM . Stay Healthy! Dr. Tangri\'s Dental Clinic +91-981-028-9955')
print (resp)

