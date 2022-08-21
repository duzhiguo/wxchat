from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time

today = datetime.now()
# start_date = os.environ['START_DATE']
city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
def getday():
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  year=time.localtime().tm_year#既可以获取当前年份，也可以指定年份
  month=time.localtime().tm_mon#既可以获取当前月份，也可以指定年月份
  day=time.localtime().tm_mday#既可以获取当前天数，也可以指定天数
  date =datetime.date(datetime(year=year,month=month,day=day))
  now_time = time.localtime()
  chinese_time = time.strftime('%Y年%m月%d日%H时%M分',now_time)
  return chinese_time+" "+week_list[date.isoweekday()-1]



today = getday()
# start_date = os.environ['START_DATE']
# birthday = os.environ['BIRTHDAY']



def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  wen = "郑州 风力 :"+str(weather['wind'])+"\n最低温度 :"+str(weather['low'])+"\n最高温度 :"+str(weather['high'])+"\n空气质量 :"+str(weather['airQuality'])
  return weather['weather'], wen

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"data":{"value":today+"\n"},"weather":{"value":wea+"\n"},"temp":{"value":temperature+"\n"},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
