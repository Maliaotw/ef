import requests
from conf.settings import LINE_TOKEN

myToken = LINE_TOKEN

def lineNotify(token=myToken, msg='', picURI=''):
    url = "https://notify-api.line.me/api/notify"
    headers = {
                "Authorization": "Bearer " + token,
                #"Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    if picURI:
        files = {'imageFile': open(picURI, 'rb')}
        r = requests.post(url, headers=headers, params=payload, files=files)
    else:
        r = requests.post(url, headers = headers, params = payload)
    return r.status_code

