# import urllib2
# import urllib
import requests

def sendSMS(apikey, numbers, sender, message):
    # data to be sent to api
    data = {'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender}
    # sending post request and saving response as response object
    r = requests.post(url = 'https://api.textlocal.in/send/', data = data)

    pastebin_url = r.text
    # print("The pastebin URL is:%s"%pastebin_url)
    return pastebin_url



# importing the requests library

resp =  sendSMS('EQyiOW++/Kc-YnYFLVStNXIcuGxy7orWhRq1quX24n', '9407833438', 'TANGRI', 'Mr/Ms. Deepak, Your appointment has been booked for 10-10-2018 at 7:00 PM . Stay Healthy! Dr. Tangri\'s Dental Clinic +91-981-028-9955')

print (resp)
