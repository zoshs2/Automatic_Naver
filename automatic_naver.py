#!/Users/yungi/anaconda3/bin/python
import urllib
import urllib.request
import requests
from urllib.parse import urlencode
from datetime import datetime
from threading import Timer
import warnings

# import your confidential information (config.py)
# The 'config.py' must include at least 'CLIENT_ID', 'CLIENT_SECRET', and 'REFRESH_TOKEN'.
import config
try:
    from config import CLUB_ID
    clubid_list = CLUB_ID

except ImportError:
    warnings.warn("CLUB_ID does not exist in 'config.py'.")
    # TODO_1 : Append the cafe id(club id) into this dictionary.
    clubid_list = {}

def writing_on_Ncafe(access_token : str, cafe_name : str, menu, subject='default_subject', content='default_content'):
    header = "Bearer " + access_token # Bearer 다음에 공백 추가
    clubid = clubid_list[cafe_name] # 카페의 고유 ID값 
    menuid = str(menu) # Exchanger Cafes' category has not applied, such as '중고나라' etc..
    url = "https://openapi.naver.com/v1/cafe/" + clubid + "/menu/" + menuid + "/articles"
    subject = urllib.parse.quote(subject)
    content = urllib.parse.quote(content)
    data = urlencode({'subject': subject, 'content': content}).encode()
    request = urllib.request.Request(url, data=data)
    request.add_header("Authorization", header)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
        print(datetime.today())
    else:
        print("Error Code:" + rescode)

def refresh_access(ncreds):
    access_url = "https://nid.naver.com/oauth2.0/token?"
    access_data = (
        "grant_type=refresh_token"
        "&client_id=%s" 
        "&client_secret=%s" 
        "&refresh_token=%s"
    ) %(ncreds.get('client_id'), ncreds.get('client_secret'), ncreds.get('refresh_token'))

    res = requests.get(access_url + access_data)

    ncreds['access_token'] = res.json()['access_token']


# Using a function 'refresh_access', you can get the initialized access_token.
# Distributed 'access_token' is only available during one hour.
# After 1 hour, you need to get a new available 'access_token' by your 'refresh_token'.
# That is why you should keep well your 'refresh_token' privately.
ncreds = {'access_token': '',
    'client_id' : config.CLIENT_ID,
    'client_secret' : config.CLIENT_SECRET,
    'refresh_token' : config.REFRESH_TOKEN} 

refresh_access(ncreds)

current_time = datetime.today()
# TODO_2 : Set the specific time when you want to upload your post.
y = datetime(2021, 7, 25, 21, 8) 

delta_t = y-current_time

secs = delta_t.seconds + 1  

# TODO_3 : Third argument must be denoted. This will refer to a dictionary variable 'clubid_list'.
# NOTE !! The fourth argument number denotes a specific category in the cafe.
# All categories has its own number. You could get information about the number by using F12 on cafe website that you interest in.
t = Timer(secs, writing_on_Ncafe, [ncreds['access_token'], 'gransaga', 1])
t.start()