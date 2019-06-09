import requests
import json
from bs4 import BeautifulSoup as bs
import telegram
import time

API_HOST = 'https://www.swexpertacademy.com/'

secret_json_file = open('secret.json', 'r')
secret_json = json.loads(secret_json_file.read())

# User info
user = secret_json['id']
password = secret_json['pwd']

# Bot token
token = secret_json['token']

bot = telegram.Bot(token=token)
def sendMsg(msg):
  bot.sendMessage(chat_id=secret_json['chatId'], text=msg) 

if time.localtime(time.time()).tm_hour == 9:
  sendMsg('I am alive')

with requests.Session() as s:
  login_req  = s.post(API_HOST + '/main/identity/anonymous/login.do', data=secret_json)
  if login_req.status_code != 200:
    raise Exception("Login Error")

  test_list_req = s.get('https://www.swexpertacademy.com/main/sst/common/userTestList.do?')
  if test_list_req.status_code != 200:
    raise Exception("User Test List Req Error")
  
  soup = bs(test_list_req.text, 'html.parser')

  list_table = str(soup.select('body > div.sub-m > div:nth-child(9) > table')[0])
  filename = 'usertestlist.txt'
  try:
    f = open(filename, "r+") 
    f.seek(0)
    data = f.read()
    if data != list_table:
      print("it's different")
      sendMsg("Check the site")
      f.seek(0)
      f.write(list_table)
      f.truncate()
  except:
    print("No file -> Create new file")
    f = open(filename, "w+")
    f.write(list_table)
  finally:
    f.close()
  


    

