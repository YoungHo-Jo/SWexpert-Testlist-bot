import requests
import json
from bs4 import BeautifulSoup as bs
import telegram
import time
import os
import hashlib

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


with requests.Session() as s:
  login_req  = s.post(API_HOST + '/main/identity/anonymous/login.do', data=secret_json)
  if login_req.status_code != 200:
    raise Exception("Login Error")

  test_list_req = s.get(API_HOST + '/main/sst/common/userTestList.do?')
  if test_list_req.status_code != 200:
    raise Exception("User Test List Req Error")
  
  soup = bs(test_list_req.content, 'html.parser', from_encoding='UTF-8')
    
  list_table = soup.select('body > div.sub-m > div > table > tbody')[0].get_text()
  list_table = list_table.replace('\n', '\n\n')

  filename = 'usertestlist.txt'
  file_path = os.path.join(script_dir, './' + filename) 
  try:
    f = open(file_path, "r+", encoding='utf-8') 
    f.seek(0)
    data = f.read()
    print(data)

    if time.localtime(time.time()).tm_hour == 9:
        sendMsg('I am alive')
        sendMsg(list_table)
       
    hash_obj = hashlib.sha256(list_table.encode('utf8'))
    hash_dig = hash_obj.hexdigest()
    print(hash_dig)
    if data != str(hash_dig):
      print(hash_dig)
      sendMsg("Check the site")
      sendMsg(list_table)
      f.seek(0)
      f.write(str(hash_dig))
      f.truncate()
  except:
    print(e)
    f = open(file_path, "w+", encoding='utf-8')
    f.write(str(hash(list_table)))
  finally:
    f.close()
  


    

