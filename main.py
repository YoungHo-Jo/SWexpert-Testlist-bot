import requests
import json
from bs4 import BeautifulSoup as bs
import telegram
import time
import os

API_HOST = 'https://www.swexpertacademy.com'
script_dir = os.path.dirname(__file__)

secret_path = os.path.join(script_dir, './secret.json')
secret_json_file = open(secret_path, 'r')
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

  test_list_req = s.get(API_HOST + '/main/sst/common/userTestList.do?')
  if test_list_req.status_code != 200:
    raise Exception("User Test List Req Error")

  soup = bs(test_list_req.text, 'html.parser')
    
  list_table = str(soup.select('body > div.sub-m > div > table > tbody')[0].encode('utf-8'))
  filename = 'usertestlist.txt'
  file_path = os.path.join(script_dir, './' + filename) 
  try:
    f = open(file_path, "r+") 
    f.seek(0)
    data = f.read()
    if data != list_table:
      sendMsg("Check the site")
      f.seek(0)
      f.write(list_table)
      f.truncate()
  except:
    f = open(file_path, "w+")
    f.write(list_table)
  finally:
    f.close()
  


    

