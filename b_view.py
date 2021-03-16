url_list = [
"https://www.bilibili.com/video/BV1u5411P72y",
"https://www.bilibili.com/video/BV1eb4y1X7VX",
"https://www.bilibili.com/video/BV1Yi4y1N7Xe",
"https://www.bilibili.com/video/BV1Hb4y1R7Eg",
"https://www.bilibili.com/video/BV1nf4y1z7PV",
"https://www.bilibili.com/video/BV1Kp4y1p7zU",
"https://www.bilibili.com/video/BV11v4y1o7JQ",
"https://www.bilibili.com/video/BV1sV411q7vP",
"https://www.bilibili.com/video/BV11v411W7rm",
"https://www.bilibili.com/video/BV1pt4y1r7df",
"https://www.bilibili.com/video/BV1hA411p7No",
"https://www.bilibili.com/video/BV1SV411h7tb",
"https://www.bilibili.com/video/BV1854y1t7BL",
"https://www.bilibili.com/video/BV1kK4y1L7km",
]

init_sleep_sec=8
play_time_sec=60
_round=1000  # 0 for unlimited

db_file = "./view.db"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import random
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


random.shuffle(url_list)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")

conn = create_connection(db_file)

def insert_record(url):
  try:
    sql = ''' INSERT INTO view(url, time) VALUES(?,?) '''
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    cur = conn.cursor()
    cur.execute(sql, (url, dt_string))
    conn.commit()
  except Error as e:
    print(e)


def view_url(url):
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  time.sleep(init_sleep_sec)
  try:
    elem = driver.find_element_by_css_selector(".bilibili-player-dm-tip-wrap")
    elem.click()
  except:
    print("Play error.")
    driver.close()
    return
  time.sleep(play_time_sec)
  driver.close()
  insert_record(url)

if _round == 0:
  while True:
    for u in url_list:
      try:
        view_url(u)
      except Exception as e:
        print(e)
else:
  for i in range(_round):
    for u in url_list:
      try:
        view_url(u)
      except Exception as e:
        print(e)


