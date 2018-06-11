import urllib.request
import urllib.parse
  
import urllib.request
import urllib.parse
 
def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
   
resp= sendSMS('EQyiOW++/Kc-YnYFLVStNXIcuGxy7orWhRq1quX24n', '9407833438',
    'TANGRI', 'Mr/Ms. Deepak, Your appointment has been booked for 10-10-2018 at 7:00 PM . Stay Healthy! Dr. Tangri\'s Dental Clinic +91-981-028-9955')
print (resp)
